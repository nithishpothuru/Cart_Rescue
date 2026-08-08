from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

from session_manager import (
    create_session,
    add_event,
    get_session,
    get_session_events,
    end_session
)

from decision_service import generate_decision

from database import client
from routes.session_routes import session_routes
from routes.event_routes import event_routes



app = Flask(__name__)

app.register_blueprint(session_routes)
app.register_blueprint(event_routes)

CORS(app)


# ============================================================
# Health Check
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "application": "CartGuard AI",
        "status": "running"
    })


# ============================================================
# MongoDB Health Check
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    try:

        client.admin.command("ping")

        return jsonify({
            "status": "healthy",
            "mongodb": "connected"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "mongodb": "disconnected",
            "error": str(e)
        }), 500


# ============================================================
# Start Session
# ============================================================

@app.route("/api/session/start", methods=["POST"])
def start_session():

    session_id = str(uuid.uuid4())

    session = create_session(session_id)

    return jsonify({
        "success": True,
        "session_id": session_id
    })


# ============================================================
# Get Real-Time CartGuard Decision
# ============================================================

@app.route("/api/session/decision", methods=["POST"])
def session_decision():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "error": "Request body is required"
        }), 400

    session_id = data.get("session_id")

    if not session_id:

        return jsonify({
            "success": False,
            "error": "session_id is required"
        }), 400

    # --------------------------------------------------------
    # Check Session
    # --------------------------------------------------------

    session = get_session(session_id)

    if not session:

        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404

    # --------------------------------------------------------
    # Get Session Events
    # --------------------------------------------------------

    events = get_session_events(session_id)

    if not events:

        return jsonify({
            "success": False,
            "error": "No events found for this session"
        }), 400

    # --------------------------------------------------------
    # Generate CartGuard Decision
    # --------------------------------------------------------

    try:

        result = generate_decision(events)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": "Decision generation failed",
            "details": str(e)
        }), 500

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return jsonify({
        "success": True,
        "session_id": session_id,
        "decision": result
    }), 200

# ============================================================
# Get Session
# ============================================================

@app.route("/api/session/<session_id>", methods=["GET"])
def session_details(session_id):

    session = get_session(session_id)

    if not session:

        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404

    return jsonify({
        "success": True,
        "session": session
    })


# ============================================================
# End Session
# ============================================================

@app.route("/api/session/<session_id>/end", methods=["POST"])
def close_session(session_id):

    session = get_session(session_id)

    if not session:

        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404

    end_session(session_id)

    return jsonify({
        "success": True,
        "message": "Session ended"
    })


# ============================================================
# Run Server
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )