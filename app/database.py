from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Setup MongoDB client and database
client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client.videotogif  # Connect to the 'videotogif' database

# Function to test the MongoDB connection
async def test_connection():
    try:
        collections = await db.list_collection_names()
        print("Connected to MongoDB! Collections:", collections)
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
