from werkzeug.security import generate_password_hash
from database import users_collection
from datetime import datetime, timezone
import uuid

# Change these values
ADMIN_EMAIL = "admin@cartrescue.ai"
ADMIN_PASSWORD = "Admin@123"
ADMIN_NAME = "Super Admin"
ADMIN_PHONE = "+919876543210"   # your phone for Twilio testing

existing = users_collection.find_one({"email": ADMIN_EMAIL})
if existing:
    print("Admin already exists")
else:
    users_collection.insert_one({
        "user_id": str(uuid.uuid4()),
        "full_name": ADMIN_NAME,
        "email": ADMIN_EMAIL,
        "phone": ADMIN_PHONE,
        "password_hash": generate_password_hash(ADMIN_PASSWORD),
        "role": "super_admin",
        "created_at": datetime.now(timezone.utc),
    })
    print("Super Admin created successfully")
    print(f"Email: {ADMIN_EMAIL}")
    print(f"Password: {ADMIN_PASSWORD}")