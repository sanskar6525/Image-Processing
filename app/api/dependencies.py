from pymongo import MongoClient
from app.config import MONGO_URI, MONGO_DB_NAME

# Create a MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]  # Select database

def get_db():
    """Dependency function to get the MongoDB instance."""
    return db
