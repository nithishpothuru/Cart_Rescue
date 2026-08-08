from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import uuid
from session_manager import create_session, get_session, get_session_events, end_session
from decision_service import generate_decision

session_routes = Blueprint("session_routes", __name__)

@session_routes.route("/api/session/start", methods=["POST"])
def start_session():
    try:
        data = request.get_json() or {}
        user_id = data.get("user_id")
        session_id = str(uuid.uuid4())
        create_session(session_id, user_id)
        return jsonify({
            "success": True,
            "message": "Session started successfully",
            "session_id": session_id,
            "status": "active"
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@session_routes.route("/api/session/decision", methods=["POST"])
def session_decision():
    data = request.get_json() or {}
    session_id = data.get("session_id")
    if not session_id:
        return jsonify({"success": False, "error": "session_id is required"}), 400

    session = get_session(session_id)
    if not session:
        return jsonify({"success": False, "error": "Session not found"}), 404

    events = get_session_events(session_id)
    if not events:
        return jsonify({"success": False, "error": "No events found for this session"}), 400

    try:
        result = generate_decision(events)
        return jsonify({
            "success": True,
            "session_id": session_id,
            "decision": result
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Decision generation failed",
            "details": str(e)
        }), 500


@session_routes.route("/api/session/<session_id>", methods=["GET"])
def session_details(session_id):
    session = get_session(session_id)
    if not session:
        return jsonify({"success": False, "error": "Session not found"}), 404
    return jsonify({"success": True, "session": session})


@session_routes.route("/api/session/<session_id>/end", methods=["POST"])
def close_session(session_id):
    session = get_session(session_id)
    if not session:
        return jsonify({"success": False, "error": "Session not found"}), 404
    end_session(session_id)
    return jsonify({"success": True, "message": "Session ended"})
