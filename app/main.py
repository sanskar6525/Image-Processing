from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.routes import router
import uvicorn

app = FastAPI(title="Image Processing API")

# Include API routes
app.include_router(router)

# Serve static files (processed images)
app.mount("/static", StaticFiles(directory="image_processing_data/processed_images"), name="static")

@app.get("/")
def home():

    return {"message": "Image Processing API is running!"}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)