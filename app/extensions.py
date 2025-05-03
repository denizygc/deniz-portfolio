from pymongo import MongoClient
from app.config import Config

print(Config.MONGO_URI)
client = MongoClient(Config.MONGO_URI)
db = client["deniz_portfolio"] 
