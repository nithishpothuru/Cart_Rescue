from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
from database import (
    sessions_collection,
    events_collection,
    decisions_collection,
    users_collection
)
from session_manager import get_session, get_session_events
from decision_service import generate_decision
from twilio_service import send_sms, make_call
import uuid

admin_routes = Blueprint("admin_routes", __name__)


def require_admin(user_id):
    """Helper to check if user is super_admin"""
    user = users_collection.find_one({"user_id": user_id})
    if not user or user.get("role") != "super_admin":
        return False
    return True


# ============================================================
# DASHBOARD OVERVIEW
# ============================================================
@admin_routes.route("/api/admin/dashboard", methods=["GET"])
def dashboard():
    user_id = request.args.get("user_id")
    if not require_admin(user_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    total_sessions = sessions_collection.count_documents({})
    active_sessions = sessions_collection.count_documents({"status": "active"})
    high_risk = sessions_collection.count_documents({"risk_level": "HIGH"})
    total_customers = users_collection.count_documents({"role": "customer"})

    # Recent decisions
    recent_actions = list(
        decisions_collection.find({}, {"_id": 0})
        .sort("created_at", -1)
        .limit(10)
    )

    return jsonify({
        "success": True,
        "stats": {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "high_risk_sessions": high_risk,
            "total_customers": total_customers,
        },
        "recent_actions": recent_actions
    })


# ============================================================
# LIVE SESSIONS
# ============================================================
# ============================================================
# LIVE / ALL SESSIONS (with status)
# ============================================================
@admin_routes.route("/api/admin/sessions/live", methods=["GET"])
def live_sessions():
    user_id = request.args.get("user_id")
    if not require_admin(user_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    sessions = list(
        sessions_collection.find(
            {},
            {"_id": 0}
        ).sort("last_activity", -1).limit(100)
    )

    # Simple status
    for s in sessions:
        if s.get("status") == "active" or s.get("active") is True:
            s["status"] = "active"
        else:
            s["status"] = "inactive"

    return jsonify({"success": True, "sessions": sessions})


# ============================================================
# HIGH RISK SESSIONS
# ============================================================
@admin_routes.route("/api/admin/sessions/high-risk", methods=["GET"])
def high_risk_sessions():
    user_id = request.args.get("user_id")
    if not require_admin(user_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    sessions = list(
        sessions_collection.find(
            {"risk_level": "HIGH"},
            {"_id": 0}
        ).sort("last_activity", -1).limit(50)
    )

    for s in sessions:
        if s.get("status") == "active" or s.get("active") is True:
            s["status"] = "active"
        else:
            s["status"] = "inactive"

    return jsonify({"success": True, "sessions": sessions})


# ============================================================
# GET SINGLE SESSION + AI DECISION
# ============================================================
@admin_routes.route("/api/admin/sessions/<session_id>", methods=["GET"])
def get_session_detail(session_id):
    user_id = request.args.get("user_id")
    if not require_admin(user_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    session = get_session(session_id)
    if not session:
        return jsonify({"success": False, "error": "Session not found"}), 404

    events = get_session_events(session_id)

    # Generate fresh decision
    decision = None
    try:
        if events:
            decision = generate_decision(events)
            # Save risk on session
            sessions_collection.update_one(
                {"session_id": session_id},
                {"$set": {
                    "risk_score": decision["risk"]["risk_score"],
                    "risk_level": decision["risk"]["risk_level"],
                    "scenario": decision["scenario"]["scenario"],
                    "recommended_action": decision["decision"]["action"],
                }}
            )
    except Exception as e:
        print("Decision error:", e)

    return jsonify({
        "success": True,
        "session": session,
        "events": events,
        "decision": decision
    })


# ============================================================
# ACCEPT / IGNORE ACTION
# ============================================================
@admin_routes.route("/api/admin/sessions/<session_id>/action", methods=["POST"])
def handle_action(session_id):
    data = request.get_json() or {}
    user_id = data.get("user_id")
    action_choice = data.get("choice")          # "accept" or "ignore"
    suggested_action = data.get("suggested_action")
    customer_phone = data.get("customer_phone")

    if not require_admin(user_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    if action_choice not in ["accept", "ignore"]:
        return jsonify({"success": False, "error": "Invalid choice"}), 400

    # Log the decision
    decision_record = {
        "decision_id": str(uuid.uuid4()),
        "session_id": session_id,
        "admin_id": user_id,
        "suggested_action": suggested_action,
        "choice": action_choice,
        "created_at": datetime.now(timezone.utc),
        "twilio_result": None
    }

    # If accepted → trigger Twilio
    if action_choice == "accept" and customer_phone:
        message = (
            f"Hi! This is CartRescue AI. "
            f"We noticed you left items in your cart. "
            f"Complete your purchase now and enjoy a special offer. "
            f"Reply HELP for support."
        )

        # Decide SMS or Call based on action type
        if suggested_action in ["SEND_CART_REMINDER", "SHOW_EXIT_INTENT_POPUP", "SHOW_LIMITED_TIME_DISCOUNT"]:
            result = send_sms(customer_phone, message)
            decision_record["twilio_result"] = {"type": "sms", **result}
        elif suggested_action in ["OFFER_COD_OR_ALTERNATE_PAYMENT", "OFFER_FREE_SHIPPING"]:
            result = make_call(customer_phone, message)
            decision_record["twilio_result"] = {"type": "call", **result}
        else:
            result = send_sms(customer_phone, message)
            decision_record["twilio_result"] = {"type": "sms", **result}

    decisions_collection.insert_one(decision_record)

    # Update session
    sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": {
            "admin_action": action_choice,
            "admin_action_at": datetime.now(timezone.utc)
        }}
    )

    return jsonify({
        "success": True,
        "message": f"Action {action_choice}ed successfully",
        "decision": {
            "decision_id": decision_record["decision_id"],
            "choice": action_choice,
            "twilio_result": decision_record.get("twilio_result")
        }
    })


# ============================================================
# ACTION HISTORY
# ============================================================
@admin_routes.route("/api/admin/actions", methods=["GET"])
def action_history():
    user_id = request.args.get("user_id")
    if not require_admin(user_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    actions = list(
        decisions_collection.find({}, {"_id": 0})
        .sort("created_at", -1)
        .limit(100)
    )

    return jsonify({"success": True, "actions": actions})


# ============================================================
# ANALYTICS
# ============================================================
@admin_routes.route("/api/admin/analytics", methods=["GET"])
def analytics():
    user_id = request.args.get("user_id")
    if not require_admin(user_id):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    total_sessions = sessions_collection.count_documents({})
    high_risk = sessions_collection.count_documents({"risk_level": "HIGH"})
    medium_risk = sessions_collection.count_documents({"risk_level": "MEDIUM"})
    low_risk = sessions_collection.count_documents({"risk_level": "LOW"})
    accepted = decisions_collection.count_documents({"choice": "accept"})
    ignored = decisions_collection.count_documents({"choice": "ignore"})

    # Scenario breakdown
    pipeline = [
        {"$group": {"_id": "$scenario", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    scenarios = list(sessions_collection.aggregate(pipeline))

    return jsonify({
        "success": True,
        "analytics": {
            "total_sessions": total_sessions,
            "risk_breakdown": {
                "HIGH": high_risk,
                "MEDIUM": medium_risk,
                "LOW": low_risk
            },
            "actions": {
                "accepted": accepted,
                "ignored": ignored
            },
            "scenarios": scenarios
        }
    })
