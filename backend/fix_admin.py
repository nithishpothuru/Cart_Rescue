from werkzeug.security import generate_password_hash
from database import users_collection
from datetime import datetime, timezone
import uuid

ADMIN_EMAIL = "admin@cartrescue.ai"
ADMIN_PASSWORD = "Admin@123"

# Delete old admin if exists
users_collection.delete_many({"email": ADMIN_EMAIL})

# Create fresh super admin
users_collection.insert_one({
    "user_id": str(uuid.uuid4()),
    "full_name": "Super Admin",
    "email": ADMIN_EMAIL,
    "phone": "+919876543210",
    "password_hash": generate_password_hash(ADMIN_PASSWORD),
    "role": "super_admin",
    "created_at": datetime.now(timezone.utc),
})

print("✅ Super Admin created / fixed successfully")
print("Email:", ADMIN_EMAIL)
print("Password:", ADMIN_PASSWORD)
print("Role: super_admin")