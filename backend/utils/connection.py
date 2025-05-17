from pymongo import MongoClient
import os

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_USER =  os.getenv("MONGO_USER")
MONGO_PASS =  os.getenv("MONGO_PASS")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_HOST = os.getenv("MONGO_HOST")

mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB_NAME]
