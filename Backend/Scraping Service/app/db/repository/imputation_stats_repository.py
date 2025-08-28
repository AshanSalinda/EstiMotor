from app.db.database import database
from app.utils.logger import err, info
from datetime import datetime, timezone


class ImputationStats:
    def __init__(self):
        self.collection = None
        self.collection_name = "imputation_stats"

    def set_collection(self) -> None:
        """Ensures the collection is set before using it."""
        if self.collection is None:
            if database.db is None:
                raise Exception("Database connection is not initialized.")
            self.collection = database.db[self.collection_name]

    def save(self, document: dict) -> None:
        """Saves dictionary to the database."""
        try:
            self.set_collection()
            self.collection.insert_one(document)
            info("Imputation stats saved to the database.")
        except Exception as e:
            err(f"Failed to save data to the {self.collection_name} database. Error: {e}")

    def get_stats(self) -> dict:
        """Returns document in the 'imputation_stats' collection as a dictionary without '_id'."""
        try:
            self.set_collection()
            document = self.collection.find_one()

            if document:
                document.pop("_id", None)  # Remove '_id' if it exists
                return document  # Return as a dictionary

            return {}

        except Exception as e:
            err(f"Failed to get imputation stats from the database. Error: {e}")
            return {}

    def drop(self) -> None:
        """Drops the 'imputation_stats' collection."""
        try:
            self.set_collection()
            self.collection.drop()
            info("'imputation_stats' collection dropped.")
        except Exception as e:
            err(f"Failed to drop {self.collection_name} collection. Error: {e}")


imputation_stats_repo = ImputationStats()
