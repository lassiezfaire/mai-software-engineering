import os

from pymongo import MongoClient

try:
    mongo_client = MongoClient(os.getenv("MONGO_URI"))
    database = mongo_client[os.getenv("DB_NAME")]

    print("Connected to MongoDB")
except Exception as e:
    print(f"Error: {e}")
