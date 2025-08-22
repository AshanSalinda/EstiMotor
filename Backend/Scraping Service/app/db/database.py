from pymongo import MongoClient
from app.config import settings
from app.utils.logger import err, info


class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(settings.MONGO_URI)
            self.client.admin.command('ping')
            self.db = self.client[settings.DATABASE_NAME]
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
