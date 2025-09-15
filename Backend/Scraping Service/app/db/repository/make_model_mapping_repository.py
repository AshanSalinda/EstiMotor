from app.db.database import database
from app.utils.logger import err, info


class MakeModelMapping:
    def __init__(self):
        self.collection_name = "make_model_mapping"

        if database.db is None:
            raise Exception("Database connection is not initialized.")
        self.collection = database.db[self.collection_name]


    def save(self, docs: list) -> None:
        """Saves multiple documents."""
        if not docs:
            return

        try:
            self.collection.insert_many(docs)
            info("Vehicles saved to the database.")

        except Exception as e:
            err(f"Failed to save items to the {self.collection_name} database. Error: {e}")


    def drop(self) -> None:
        """Drops the collection."""
        try:
            self.collection.drop()
            info("'make_model_category' collection dropped.")
        except Exception as e:
            err(f"Failed to drop {self.collection_name} collection. Error: {e}")


make_model_mapping_repo = MakeModelMapping()
