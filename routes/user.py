from fastapi import APIRouter, HTTPException,Query
from models.model import RegisterForm
from config.config import user_collection
from bson import ObjectId
import bcrypt 

# Create a router for user-related routes
user = APIRouter()

@user.post("/register")
async def register_user(user: RegisterForm):
    try:
        # Check if the email already exists
        existing_user = user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hased_pass = bcrypt.hashpw(user.password.encode('utf-8'),bcrypt.gensalt())

        # Insert the new user into the database
        new_user = {
            "name": user.name,
            "email": user.email,
            "password": hased_pass.decode('utf-8') # In a real app, hash the password!
        }
        result = user_collection.insert_one(new_user)

        # Return a success response with the new user's ID
        return {"message": "User registered successfully!", "user_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@user.get("/users")
async def get_users(user_id: str = Query(None, description="ID of the user to fetch (optional)")):
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
                raise HTTPException(status_code=400, detail="Invalid user ID format")

            # Fetch the specific user
            user = user_collection.find_one({"_id": user_object_id}, {"_id": 0})  # Exclude '_id' from response if not needed
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"user": user}

        # Fetch all users if no user_id is provided
        users = list(user_collection.find({}, {"_id": 0}))  # Exclude '_id' from response if not needed
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return {"users": users}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
    
