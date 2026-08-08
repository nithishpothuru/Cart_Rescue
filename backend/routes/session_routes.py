from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import uuid

session_routes = Blueprint("session_routes", __name__)


def get_db():
    from database import get_database
    return get_database()


@session_routes.route("/api/session/start", methods=["POST"])
def start_session():

    try:
        data = request.get_json() or {}

        user_id = data.get("user_id")

        session_id = str(uuid.uuid4())

        session = {
            "session_id": session_id,
            "user_id": user_id,

            "status": "active",

            "started_at": datetime.now(timezone.utc),
            "last_activity": datetime.now(timezone.utc),

            "cart_value": 0.0,
            "cart_items": 0,

            "risk_score": None,
            "risk_level": None,

            "scenario": None,
            "recommended_action": None
        }

        db = get_db()

        db.sessions.insert_one(session)

        return jsonify({
            "success": True,
            "message": "Session started successfully",
            "session_id": session_id,
            "status": "active"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500