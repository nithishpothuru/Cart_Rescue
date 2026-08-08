from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

from database import sessions_collection, events_collection


event_routes = Blueprint("event_routes", __name__)


@event_routes.route("/api/session/event", methods=["POST"])
def add_event():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required."
            }), 400

        session_id = data.get("session_id")
        event_type = data.get("event_type")

        if not session_id:
            return jsonify({
                "success": False,
                "error": "session_id is required."
            }), 400

        if not event_type:
            return jsonify({
                "success": False,
                "error": "event_type is required."
            }), 400

        # Check session
        session = sessions_collection.find_one({
            "session_id": session_id
        })

        if not session:
            return jsonify({
                "success": False,
                "error": "Session not found."
            }), 404

        # Create event
        event = {
            "session_id": session_id,
            "event_type": event_type,

            "product_id": data.get("product_id"),
            "category": data.get("category"),
            "category_id": data.get("category_id"),
            "brand": data.get("brand"),
            "price": float(data.get("price", 0)),

            "payment_method": data.get("payment_method"),
            "payment_status": data.get("payment_status"),

            "timestamp": datetime.now(timezone.utc),
            "event_time": datetime.now(timezone.utc)
        }

        result = events_collection.insert_one(event)

        # Update session activity
        sessions_collection.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "last_activity": datetime.now(timezone.utc)
                }
            }
        )

        return jsonify({
            "success": True,
            "message": "Event recorded successfully.",
            "event_id": str(result.inserted_id),
            "session_id": session_id,
            "event_type": event_type
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500