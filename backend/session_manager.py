from datetime import datetime, timezone

from database import (
    sessions_collection,
    events_collection
)


# ============================================================
# CREATE SESSION
# ============================================================

def create_session(session_id):

    session = {
        "session_id": session_id,
        "started_at": datetime.now(timezone.utc),
        "last_activity": datetime.now(timezone.utc),
        "active": True
    }

    sessions_collection.insert_one(session)

    return session


# ============================================================
# ADD EVENT
# ============================================================

def add_event(session_id, event):

    event_data = {
        "session_id": session_id,
        "event_type": event,
        "timestamp": datetime.now(timezone.utc)
    }

    events_collection.insert_one(event_data)

    sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "last_activity": datetime.now(timezone.utc)
            }
        }
    )

    return True


# ============================================================
# GET SESSION
# ============================================================

def get_session(session_id):

    return sessions_collection.find_one(
        {"session_id": session_id},
        {"_id": 0}
    )


# ============================================================
# GET SESSION EVENTS
# ============================================================

def get_session_events(session_id):

    events = list(
        events_collection.find(
            {"session_id": session_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )

    return events


# ============================================================
# END SESSION
# ============================================================

def end_session(session_id):

    sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "active": False,
                "ended_at": datetime.now(timezone.utc)
            }
        }
    )

    return Truex