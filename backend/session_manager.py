from datetime import datetime, timezone
from database import sessions_collection, events_collection

def create_session(session_id, user_id=None):
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
        "recommended_action": None,
    }
    sessions_collection.insert_one(session)
    return session

def add_event(session_id, event_data):
    event = {
        "session_id": session_id,
        "event_type": event_data.get("event_type"),
        "product_id": event_data.get("product_id"),
        "category": event_data.get("category"),
        "brand": event_data.get("brand"),
        "price": float(event_data.get("price", 0)),
        "payment_method": event_data.get("payment_method"),
        "payment_status": event_data.get("payment_status"),
        "timestamp": datetime.now(timezone.utc),
        "event_time": datetime.now(timezone.utc),
    }
    events_collection.insert_one(event)

    sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": {"last_activity": datetime.now(timezone.utc)}}
    )
    return True

def get_session(session_id):
    return sessions_collection.find_one({"session_id": session_id}, {"_id": 0})

def get_session_events(session_id):
    return list(
        events_collection.find(
            {"session_id": session_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )

def end_session(session_id):
    sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "status": "ended",
                "ended_at": datetime.now(timezone.utc),
            }
        },
    )
    return True
    