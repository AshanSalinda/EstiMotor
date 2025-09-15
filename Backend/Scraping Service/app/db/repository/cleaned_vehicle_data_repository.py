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

    def get_make_model_category_map(self) -> list:
        """Builds and returns a mapping of makes → models → categories."""
        try:
            self.set_collection()
            pipeline = [
                # 1. Count occurrences of each (make, model, category)
                {
                    "$group": {
                        "_id": {"make": "$make", "model": "$model", "category": "$category"},
                        "count": {"$sum": 1}
                    }
                },
                # 2. Sort by make, model, count descending
                {
                    "$sort": {"_id.make": 1, "_id.model": 1, "count": -1}
                },
                # 3. Group by make + model, pick first category (most frequent)
                {
                    "$group": {
                        "_id": {"make": "$_id.make", "model": "$_id.model"},
                        "category": {"$first": "$_id.category"}
                    }
                },
                # 4. Group by make → collect models with their single category
                {
                    "$group": {
                        "_id": "$_id.make",
                        "models": {
                            "$push": {"name": "$_id.model", "category": "$category"}
                        }
                    }
                },
                # 5. Final projection
                {
                    "$project": {"_id": 0, "make": "$_id", "models": 1}
                }
            ]

            info(f"Fetched make-model-category mapping from the database.")
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            err(f"Failed to build make-model-category mapping. Error: {e}")
            return []

    def drop(self) -> None:
        """Drops the 'vehicle' collection."""
        try:
            self.set_collection()
            self.collection.drop()
            info("vehicle collection dropped.")
        except Exception as e:
            err(f"Failed to drop vehicles collection. Error: {e}")


cleaned_vehicles_data_repo = CleanedVehicles()
