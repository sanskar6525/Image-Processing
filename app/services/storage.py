from pymongo import MongoClient
from app.api.dependencies import get_db

db = get_db()

def save_request(request_id: str, data: list):
    """Save a new image processing request to MongoDB."""
    db.requests.insert_one({
        "request_id": request_id,
        "status": "processing",
        "data": data
    })

def update_request_status(request_id: str, index, output_images):
    """Update processing status and output images for a specific request."""
    if index == "completed":
        db.requests.update_one(
            {"request_id": request_id},
            {"$set": {"status": "completed"}}
        )
    else:
        db.requests.update_one(
            {"request_id": request_id},
            {"$set": {f"data.{index}.Output Image Urls": output_images}}
        )

def get_request_status(request_id: str):
    """Retrieve the status of a processing request."""
    return db.requests.find_one({"request_id": request_id}, {"_id": 0})
