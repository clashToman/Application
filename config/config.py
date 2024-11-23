import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get MongoDB credentials from environment variables
username = quote_plus(os.getenv("MONGO_USERNAME", "default_username"))
password = quote_plus(os.getenv("MONGO_PASSWORD", "default_password"))

# Construct the MongoDB URI with encoded username and password
uri = f"mongodb+srv://{username}:{password}@cluster0.ztr6g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB using pymongo
client = MongoClient(uri)

# Access the desired database
db = client.get_database("myBlogs")

# Collections
user_collection = db["users"]
product_collection = db["Product"]

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
    # Test MongoDB connection
    client.admin.command("ping")
    print("Connection successful...!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
