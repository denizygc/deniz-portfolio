import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    MONGO_URI = os.environ.get("MONGO_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    PUBLIC_KEY= os.environ.get("PUBLIC_KEY")
    PRIVATE_KEY= os.environ.get("PRIVATE_KEY")
    PROJECT_ID= os.environ.get("PROJECT_ID")