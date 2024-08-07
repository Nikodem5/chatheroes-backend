from pymongo import MongoClient
from config import config

def get_db():
    client = MongoClient(config.MONGODB_URI)
    db = client["MainBase"]
    return db