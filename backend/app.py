from flask import Flask, jsonify
from flask_cors import CORS
from database import test_connection
from routes.session_routes import session_routes
from routes.event_routes import event_routes
from routes.auth_routes import auth_routes
from routes.product_routes import product_routes
from routes.admin_routes import admin_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(session_routes)
app.register_blueprint(event_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(product_routes)
app.register_blueprint(admin_routes)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": "CartRescue AI",
        "status": "running",
        "version": "1.0"
    })

@app.route("/health", methods=["GET"])
def health():
    ok = test_connection()
    return jsonify({
        "status": "healthy" if ok else "error",
        "mongodb": "connected" if ok else "disconnected"
    }), 200 if ok else 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
