from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup MongoDB client and database
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is not set")

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()  # Automatically connect to the default database in the URI
users_collection = db.get_collection("users")  # Access the 'users' collection
