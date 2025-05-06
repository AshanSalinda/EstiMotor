from app.db.database import database
from app.utils.logger import err, info


class CleanedVehicles:
    def __init__(self):
        self.collection = None
        self.collection_name = "cleaned_vehicle_data"

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
            err(f"Failed to save vehicles to the database. Error: {e}")

    def drop(self) -> None:
        """Drops the 'vehicle' collection."""
        try:
            self.set_collection()
            self.collection.drop()
            info("vehicle collection dropped.")
        except Exception as e:
            err(f"Failed to drop vehicles collection. Error: {e}")


cleaned_vehicles_data_repo = CleanedVehicles()
