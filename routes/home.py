from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os
import shutil

home_router = APIRouter()

# Directory to store uploaded images
UPLOAD_DIR = "uploads_image"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory database for offers
offers_db = []

@home_router.post("/upload/")
async def upload_offer(file: UploadFile = File(...), offer: str = Form("")):
    """Upload an image with an offer description."""
    # Ensure the filename is a string
    file_name = str(file.filename)
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Store offer details
    offer_data = {
        "filename": file_name,
        "offer": offer,
        "url": f"/uploads_images/{file_name}"
    }
    offers_db.append(offer_data)

    return JSONResponse(content={"message": "Upload successful", "data": offer_data})


@home_router.get("/offers/")
async def list_offers():
    """List all uploaded images with their offers."""
    return JSONResponse(content={"offers": offers_db})
