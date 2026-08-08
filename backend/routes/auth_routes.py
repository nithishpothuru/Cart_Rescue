from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from database import users_collection
import uuid

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json() or {}
        
        full_name = data.get("full_name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        # Only allow "customer" from public register. Admin is created manually.
        role = "customer"

        if not full_name or not email or not password:
            return jsonify({
                "success": False,
                "error": "Full name, email and password are required"
            }), 400

        existing = users_collection.find_one({"email": email.lower().strip()})
        if existing:
            return jsonify({
                "success": False,
                "error": "Email already registered"
            }), 409

        user = {
            "user_id": str(uuid.uuid4()),
            "full_name": full_name,
            "email": email.lower().strip(),
            "phone": phone,
            "password_hash": generate_password_hash(password),
            "role": role,                    # "customer" or "super_admin"
            "created_at": datetime.now(timezone.utc),
        }

        users_collection.insert_one(user)

        return jsonify({
            "success": True,
            "message": "Account created successfully",
            "user": {
                "user_id": user["user_id"],
                "full_name": full_name,
                "email": email,
                "role": role,
                "phone": phone
            }
        }), 201

    except Exception as e:
        print("Register Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


@auth_routes.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}
        email = data.get("email", "").lower().strip()
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "success": False,
                "error": "Email and password required"
            }), 400

        user = users_collection.find_one({"email": email})
        
        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify({
                "success": False,
                "error": "Invalid email or password"
            }), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user.get("role", "customer"),
                "phone": user.get("phone")
            }
        }), 200

    except Exception as e:
        print("Login Error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500