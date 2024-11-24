from fastapi import APIRouter, HTTPException, status
from config.config import user_collection, EMAIL_CONF
from fastapi_mail import FastMail, MessageSchema
from datetime import datetime, timedelta
from models.model import EmailRequest, OtpVerfication
import random
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router and email client
router = APIRouter()
fast_mail = FastMail(EMAIL_CONF)


# Utility function for email validation
def validate_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


# Generate and send OTP
@router.post("/send-otp")
async def send_otp(email_request: EmailRequest):
    email = email_request.email

    # Validate email format
    if not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format"
        )

    try:
        # Check if the user already exists and is verified
        user = user_collection.find_one({"email": email})
        if user and user.get("is_verified", False):
            return {"message": "You are already our client!"}

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)

        # Update or create user in the database
        if not user:
            user = {
                "email": email,
                "username": f"user_{random.randint(1000, 9999)}",
                "created_at": datetime.utcnow(),
                "is_verified": False,  # Add a verification status field
            }
            user_collection.insert_one(user)

        user_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "otp": otp,
                    "otp_expiry": datetime.utcnow() + timedelta(minutes=5),
                }
            },
        )

        # Prepare the email
        message = MessageSchema(
            subject="Your OTP Code",
            recipients=[email],
            body=f"Hello,\n\nYour OTP code is: {otp}\n\nThis code will expire in 5 minutes.",
            subtype="plain",  # type:ignore
        )

        # Send the email
        try:
            await fast_mail.send_message(message)
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email",
            )

        return {"message": "OTP sent to your email"}

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Verify OTP
@router.post("/verify-otp")
async def verify_otp(otp_request: OtpVerfication):
    email = otp_request.email
    otp = otp_request.otp

    try:
        # Check if the user exists in the database
        user = user_collection.find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered"
            )

        # Check if the user is already verified
        if user.get("is_verified", False):
            return {"message": "You are already our client!"}

        # Check if OTP exists and matches
        if not user.get("otp") or user["otp"] != otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
            )

        # Check if OTP is expired
        if user.get("otp_expiry") and user["otp_expiry"] < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired"
            )

        # Mark user as verified and clear OTP
        user_collection.update_one(
            {"email": email},
            {
                "$set": {"is_verified": True},
                "$unset": {"otp": "", "otp_expiry": ""},
            },
        )

        logger.info(f"OTP verified successfully for {email}")
        return {
            "message": "Login successful",
            "user": {"username": user["username"], "email": user["email"]},
        }

    except Exception as e:
        # Log the error and raise a 500 Internal Server Error
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
