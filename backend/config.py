import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "cartguard")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing from .env")