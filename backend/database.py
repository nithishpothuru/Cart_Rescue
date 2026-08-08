from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

sessions_collection = db["sessions"]
events_collection = db["events"]
decisions_collection = db["decisions"]
users_collection = db["users"]
products_collection = db["products"]
carts_collection = db["carts"]

def get_database():
    return db

def test_connection():
    try:
        client.admin.command("ping")
        print("✅ MongoDB connected")
        return True
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
        return False
