import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app.utils.logger import err, info

load_dotenv()

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Connect to MongoDB."""
        try:
            mongo_uri = os.getenv("MONGO_URI")
            database_name = os.getenv("DATABASE_NAME")

            if not mongo_uri:
                err("MONGO_URI is not set in environment variables!")
                exit(1)
            if not database_name:
                err("DATABASE_NAME is not set in environment variables!")
                exit(1)

            self.client = MongoClient(mongo_uri)
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            info("MongoDB Connected.")

        except Exception as e:
            err("Failed to connect to MongoDB:")
            print("error", e)

    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            info("MongoDB connection closed.")


# Create a global instance
database = Database()
