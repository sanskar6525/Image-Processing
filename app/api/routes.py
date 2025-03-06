from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
import pandas as pd
import os
import requests
import uuid
from PIL import Image
from io import BytesIO
from app.api.dependencies import get_db

router = APIRouter()

# Store images in a writable directory instead of using GridFS
PROCESSED_DIR = os.path.expanduser("image_processing_data/processed_images")  # Change as needed
os.makedirs(PROCESSED_DIR, exist_ok=True)

def process_images(request_id: str, file_data: bytes, db):
    """Process images asynchronously by compressing and storing them locally with URLs in MongoDB."""
    print(f"🔄 Processing started for request_id: {request_id}")

    df = pd.read_csv(BytesIO(file_data))
    processed_images = []

    for index, row in df.iterrows():
        product_name = row["Product Name"]
        image_urls = row["Input Image Urls"].split(",")
        output_image_urls = []

        for image_url in image_urls:
            response = requests.get(image_url.strip())
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img = img.convert("RGB")

                # Compress image and save to local storage
                filename = f"{uuid.uuid4()}_{product_name}.jpg"
                output_path = os.path.join(PROCESSED_DIR, filename)
                img.save(output_path, "JPEG", quality=50)  # 50% quality compression

                # Generate a public URL for the image (adjust based on deployment)
                image_url = f"http://localhost:8000/static/{filename}"
                output_image_urls.append(image_url)

        # Store in MongoDB
        db.requests.update_one(
            {"request_id": request_id},
            {"$push": {"data": {
                "serial_number": row["Serial Number"],
                "product_name": product_name,
                "input_image_urls": image_urls,
                "output_image_urls": output_image_urls  # Storing URLs instead of file IDs
            }}}
        )

    db.requests.update_one({"request_id": request_id}, {"$set": {"status": "completed"}})
    print(f"Processing completed for request_id: {request_id}")

@router.post("/upload/")
async def upload_csv(file: UploadFile = File(...), background_tasks: BackgroundTasks = None, db=Depends(get_db)):
    """Upload CSV and process images asynchronously, storing compressed image URLs in MongoDB."""
    file_data = await file.read()  # Read CSV as bytes

    # Validate CSV format
    df = pd.read_csv(BytesIO(file_data))
    if "Serial Number" not in df.columns or "Product Name" not in df.columns or "Input Image Urls" not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid CSV format")

    print("File passed the validation check")

    # Generate request_id
    request_id = str(uuid.uuid4())

    # Store request metadata in MongoDB
    db.requests.insert_one({"request_id": request_id, "status": "processing", "data": []})

    # Start processing in the background
    background_tasks.add_task(process_images, request_id, file_data, db)

    return {"message": "Processing started in the background", "request_id": request_id}

@router.get("/status/{request_id}")
async def get_status(request_id: str, db=Depends(get_db)):
    """Check processing status from MongoDB."""
    request_data = db.requests.find_one({"request_id": request_id}, {"_id": 0})
    if not request_data:
        raise HTTPException(status_code=404, detail="Request ID not found")

    return request_data

@router.post("/webhook/")
async def webhook_listener(data: dict):
    """Receives webhook notifications."""
    request_id = data.get("request_id")
    status = data.get("status")

    if not request_id or not status:
        raise HTTPException(status_code=400, detail="Missing request_id or status")

    print(f"Webhook received: Request ID: {request_id}, Status: {status}")
    return {"message": "Webhook received successfully"}

