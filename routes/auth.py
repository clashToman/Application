from fastapi import APIRouter, HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from config.config import user_collection, EMAIL_CONF, SECRET_KEY, ALGORITHM
from fastapi_mail import FastMail, MessageSchema
from datetime import datetime, timedelta
from jose import jwt, JWTError
import random
import re
from models.model import EmailRequest, OtpVerification

router = APIRouter()
fast_mail = FastMail(EMAIL_CONF)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Helper function to generate user ID (like user1, user2)
def generate_user_id():
    last_user = user_collection.find_one({}, sort=[("user_id", -1)])
    if last_user and "user_id" in last_user:
        last_id = int(last_user["user_id"].replace("user", ""))
        return f"user{last_id + 1}"
    return "user1"

# Utility function for email validation
def validate_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None

# Generate Access Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode Token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    email = decode_token(token)
    if email is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = user_collection.find_one({"email": email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Add "sub" key for compatibility with order placement logic
    user["sub"] = email
    return user


# Send OTP (with bypass for existing users)
@router.post("/send-otp")
async def send_otp(request: EmailRequest):
    email = request.email

    # Validate email format
    if not validate_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format")

    user = user_collection.find_one({"email": email})

    if user:
        # Existing user: Skip OTP, directly issue access token
        username = user.get("username", "User")
        access_token = create_access_token({"sub": email})
        return {
            "message": f"Welcome back, {username}!",
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        # New user: Generate OTP and send it
        otp = random.randint(100000, 999999)
        expiry_time = datetime.utcnow() + timedelta(minutes=5)
        user_collection.insert_one({"email": email, "otp": otp, "otp_expiry": expiry_time})

        message_text = f"Your OTP code is: {otp}. It expires in 5 minutes."

        # Send OTP via email
        message = MessageSchema(
            subject="Your OTP Code",
            recipients=[email],
            body=message_text,
            subtype="plain"#type:ignore
        )
        await fast_mail.send_message(message)

        return {"message": "OTP sent successfully"}


# Verify OTP and create user if new
@router.post("/verify-otp")
async def verify_otp(request: OtpVerification):
    user = user_collection.find_one({"email": request.email})
    if not user or user.get("otp") != request.otp or user.get("otp_expiry") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Clear OTP after successful verification
    user_collection.update_one({"email": request.email}, {"$unset": {"otp": "", "otp_expiry": ""}})

    # Mark user as verified
    user_collection.update_one({"email": request.email}, {"$set": {"is_verified": True}})

    # Create user if it doesn't exist
    if "user_id" not in user:
        new_user_id = generate_user_id()
        user_collection.update_one(
            {"email": request.email},
            {"$set": {
                "user_id": new_user_id,
                "username": request.email.split("@")[0],
                "role": "user",
                "is_verified": True
            }}
        )

    # Generate access token
    access_token = create_access_token({"sub": request.email})

    # Home page URL
    home_url = "https://yourdomain.com/home"

    return {
        "verified": True,
        "access_token": access_token,
        "token_type": "bearer",
        "redirect_url": home_url,
        "message": "User verified successfully"
    }
