from app.db.database import database
from app.utils.logger import info, err


class VehicleDataRepo:
    def __init__(self):
        self.collection = None
        self.collection_name = "cleaned_vehicle_data"

    def set_collection(self) -> None:
        """Ensures the collection is set before using it."""
        if self.collection is None:
            if database.db is None:
                raise Exception("Database connection is not initialized.")
            self.collection = database.db[self.collection_name]

    def get_all(self) -> list:
        """Fetch all vehicles from the database."""
        try:
            self.set_collection()
            vehicles = list(self.collection.find({}))
            info(f"Fetched {len(vehicles)} vehicles from the database.")
            return vehicles
        except Exception as e:
            err(f"Failed to fetch vehicles from the database. Error: {e}")
            return []


vehicle_data_repo = VehicleDataRepo()
