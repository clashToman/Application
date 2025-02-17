from fastapi import FastAPI, APIRouter, HTTPException, Depends
from config.config import  user_collection
from models.model import  RegisterForm, ProfileUpdate
from datetime import datetime

from routes.auth import get_current_user
import requests

app = FastAPI()

# Helper function to get live location
def get_live_location():
    try:
        response = requests.get("https://ipapi.co/json/")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown City")
            region = data.get("region", "Unknown Region")
            country = data.get("country_name", "Unknown Country")
            postal = data.get("postal", "Unknown Postal Code")
            return f"{city}, {region}, {country}, {postal}"
        else:
            return "Location unavailable"
    except Exception as e:
        return f"Error fetching location: {e}"

# User Router
user_router = APIRouter()

@user_router.post("/register")
def register_user(user: RegisterForm):
    existing_user = user_collection.find_one({"email": user.email})
    if not existing_user or not existing_user.get("is_verified"):
        raise HTTPException(status_code=400, detail="Email not verified or user not found")
    live_address = get_live_location()
    user_collection.update_one(
        {"email": user.email},
        {"$set": {
            "full_name": user.full_name,
            "address": live_address,
            "phone_number": user.phone_number,
            "age": user.age,
            "updated_at": datetime.utcnow(),
        }}
    )
    return {"message": "User registered successfully", "address": live_address}

@user_router.patch("/update-profile")
def update_profile(user_data: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    update_fields = {k: v for k, v in user_data.dict().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    user_collection.update_one({"user_id": user_id}, {"$set": update_fields, "$currentDate": {"updated_at": True}})
    return {"message": "Profile updated successfully"}

@user_router.get("/me")
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user