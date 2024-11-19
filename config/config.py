from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo import MongoClient


class Settings(BaseSettings):
    mongodb_url: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore

# Connect to MongoDB using pymongo
client = MongoClient(settings.mongodb_url)

# Access the desired database
db = client.get_database("myBlogs")

user_collection = db['users']
product_collection = db['Product']

try:
    # Connect to MongoDB
    
    # Access the desired database
    db = client.get_database("myBlogs")
    
    # Access the 'users' collection
    user_collection = db['users']
    
    # If the connection is successful
    print("Connection successful...!")

except ConnectionError:
    print("Failed to connect to MongoDB.")