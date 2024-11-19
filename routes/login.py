from fastapi import APIRouter, HTTPException, Request
from models.model import LoginForm, Profile
from config.config import user_collection
import bcrypt
from datetime import datetime
from bson import ObjectId

log = APIRouter()


@log.post("/login")
async def login_form(form_data: LoginForm, request: Request):
    # Find the user by email
    user = user_collection.find_one({"email": form_data.email})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check if the password matches the hashed password
    if not bcrypt.checkpw(
        form_data.password.encode("utf-8"), user["password"].encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    #request.session["USER"] = user.id

    # Get the current date and time
    login_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # Format: "YYYY-MM-DD HH:MM:SS"

    # Return a welcome message along with the login time
    return {"message": f"Welcome, {user['name']}!", "login_time": login_time}


@log.post("/logout")
async def user_logout():
    return {"Logout successfully"}


# Profile updation......!


@log.patch("/profile/{user_id}")
async def update_user_profile(user_id: str, user_data: Profile):
    try:
        # Convert user_id to ObjectId
        user = user_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare fields for update
        update_data = {}
        if user_data.name is not None:
            update_data["name"] = user_data.name
        if user_data.address is not None:
            update_data["address"] = user_data.address
        if user_data.password is not None:
            hashed_password = bcrypt.hashpw(
                user_data.password.encode("utf-8"), bcrypt.gensalt()
            )
            update_data["password"] = hashed_password.decode("utf-8")

        if not update_data:
            raise HTTPException(status_code=400, detail="No data to update")

        # Update the user
        result = user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made")

        return {"message": "User profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
