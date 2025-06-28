import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import MONGO_URI, DB_NAME
from pymongo import MongoClient


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db['sensor_data']

if __name__ == "__main__":
    print("Connected to:", DB_NAME)
