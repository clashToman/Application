from fastapi import APIRouter, HTTPException, Query, status
from models.model import RegisterForm,ProfileUpdate
from datetime import datetime
from config.config import user_collection
from bson import ObjectId


# Create a router for user-related routes
user = APIRouter()


@user.post("/register-form")
async def register_form(
    user: RegisterForm,  # RegisterForm is a Pydantic model containing the fields
):
    # Check if the user exists and is verified
    user_data = user_collection.find_one({"email": user.email})

    if not user_data:
        raise HTTPException(
            status_code=404, detail="User not found. Please verify your email first."
        )

    if not user_data.get("is_verified", False):
        raise HTTPException(
            status_code=400,
            detail="Email not verified. Please complete email verification.",
        )

    # If user exists and is verified, update their additional details
    user_collection.update_one(
        {"email": user.email},  # Match the user by email
        {
            "$set": {
                "full_name": user.name,
                "address": user.address,
                "phone": user.phone,
                "age": user.age,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    return {"message": "User details updated successfully!"}


@user.patch("/update-profile/{user_id}")
async def update_profile(
    user_id: str,  # User ID passed directly in the URL path
    user_data: ProfileUpdate,  # User data passed in the request body
):
    try:
        # Convert the user_id string to ObjectId
        user_object_id = ObjectId(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID format{e}")

    # Check if the user exists in the database
    user = user_collection.find_one({"_id": user_object_id})  # Use ObjectId here

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prepare the fields to update (only the fields provided in the request)
    update_fields = {k: v for k, v in user_data.dict().items() if v is not None}

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Update the user document in MongoDB
    result = user_collection.update_one(
        {"_id": user_object_id},  # Match the user by ObjectId
        {"$set": update_fields, "$currentDate": {"updated_at": True}}  # Update the fields and add current date
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User profile updated successfully!"}

@user.get("/users")
async def get_users(
    user_id: str = Query(None, description="ID of the user to fetch (optional)"),
):
    """
    Fetch all users if no user_id is provided.
    Fetch a specific user if user_id is provided.
    """
    try:
        if user_id:
            # Convert user_id to ObjectId
            try:
                user_object_id = ObjectId(user_id)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user ID format",
                )

            # Fetch the specific user
            user = user_collection.find_one(
                {"_id": user_object_id}, {"_id": 0}
            )  # Exclude '_id' from response if not needed
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            return {"user": user}

        # Fetch all users if no user_id is provided
        users = list(
            user_collection.find({}, {"_id": 0})
        )  # Exclude '_id' from response if not needed
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return {"users": users}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
