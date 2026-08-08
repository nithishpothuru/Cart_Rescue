from pymongo import MongoClient
import os

# ============================================================
# MongoDB Configuration
# ============================================================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "YOUR_MONGODB_ATLAS_CONNECTION_STRING"
)

DATABASE_NAME = "cart_rescue"

# ============================================================
# MongoDB Connection
# ============================================================

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

print("MongoDB connection initialized.")

# ============================================================
# Collections
# ============================================================

sessions_collection = db["sessions"]

events_collection = db["events"]

decisions_collection = db["decisions"]


# ============================================================
# Database Getter
# ============================================================

def get_database():
    return db


# ============================================================
# Collection Getters
# ============================================================

def get_sessions_collection():
    return sessions_collection


def get_events_collection():
    return events_collection


def get_decisions_collection():
    return decisions_collection


# ============================================================
# Connection Test
# ============================================================

def test_connection():

    try:

        client.admin.command("ping")

        print("MongoDB connection test successful.")

        return True

    except Exception as e:

        print("MongoDB connection test failed.")

        print(e)

        return False