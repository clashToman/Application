import os
from pymongo.mongo_client import MongoClient
from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv

load_dotenv("C:\\Users\\PRAVEEN\\OneDrive\\Desktop\\A\\.env")
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Mongo URI is not set in the .env file!")


# Connect to MongoDB using pymongo
client = MongoClient(MONGO_URI)


# Access the desired database
db = client.get_database("myBlogs")


# Collections
user_collection = db["users"]
product_collection = db["Product"]
order_collection = db["orders"]
order_history_collection = db["History"]
category_collection = db["category_Collection"]
subscription_collection = db["subscriptions_Collection"]


SECRET_KEY = "YOUR_SECRET_KEY"
REFRESH_SECRET_KEY = "YOUR_REFRESH_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# Email configuration from environment variables
EMAIL_CONF = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "default_email@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "default_password"),
    MAIL_FROM=os.getenv("MAIL_FROM", "default_email@gmail.com"),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 465)),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "False").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "True").lower() == "true",
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS", "True").lower() == "true",
)

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)

    # Access the desired database
    db = client.get_database("myBlogs")

    # Access collections
    user_collection = db["users"]
    product_collection = db["Product"]

    print("✅ Connection successful...!")

except ConnectionError as e:
    print(f"Failed to connect to MongoDB: {e}")
