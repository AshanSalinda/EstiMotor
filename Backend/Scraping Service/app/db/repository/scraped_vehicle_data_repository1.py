from bson import ObjectId

from app.db.database import database
from app.utils.logger import err, info


class ScrapedVehicles:
    def __init__(self):
        self.collection = None
        self.collection_name = "scraped_vehicle_data1"

    def set_collection(self) -> None:
        """Ensures the collection is set before using it."""
        if self.collection is None:
            if database.db is None:
                raise Exception("Database connection is not initialized.")
            self.collection = database.db[self.collection_name]

    def save(self, vehicles: list) -> None:
        """Saves all vehicles to the database."""
        try:
            self.set_collection()
            self.collection.insert_many(vehicles)
            info("Vehicles saved to the database.")
        except Exception as e:
            err(f"Failed to save data to the {self.collection_name} database. Error: {e}")

    def get_paginated(self, page: int = 1, page_size: int = 50) -> list:
        """Returns a paginated list of vehicle documents."""
        try:
            self.set_collection()
            skip = (page - 1) * page_size
            cursor = self.collection.find().skip(skip).limit(page_size)
            return list(cursor)
        except Exception as e:
            err(f"Failed to get paginated vehicles. Error: {e}")
            return []

    def delete_by_ids(self, ids: list) -> None:
        """Deletes multiple vehicle documents by their _id."""
        try:
            self.set_collection()
            object_ids = [ObjectId(_id) for _id in ids]
            result = self.collection.delete_many({"_id": {"$in": object_ids}})
            info(f"Deleted {result.deleted_count} vehicles from {self.collection_name}.")
        except Exception as e:
            err(f"Failed to delete vehicles by ids from {self.collection_name}. Error: {e}")

    def drop(self) -> None:
        """Drops the 'vehicle' collection."""
        try:
            self.set_collection()
            self.collection.drop()
            info(f"{self.collection_name} collection dropped.")
        except Exception as e:
            err(f"Failed to drop {self.collection_name} collection. Error: {e}")


scraped_vehicles_data_repo = ScrapedVehicles()
