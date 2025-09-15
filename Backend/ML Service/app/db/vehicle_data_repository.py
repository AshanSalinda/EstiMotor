from app.db.database import database
from app.utils.logger import info, err


class VehicleDataRepo:
    def __init__(self):
        self.collection_name = "cleaned_vehicle_data"

        if database.db is None:
            raise Exception("Database connection is not initialized.")

        self.collection = database.db[self.collection_name]

        # Create indexes for faster queries
        self.collection.create_index([
            ("make", 1),
            ("model", 1),
            ("fuel_type", 1),
            ("transmission", 1)
        ])

    def get_all(self) -> list:
        """Fetch all vehicles from the database."""
        try:
            vehicles = list(self.collection.find({}))
            info(f"Fetched {len(vehicles)} vehicles from the database.")
            return vehicles
        except Exception as e:
            err(f"Failed to fetch vehicles from the database. Error: {e}")
            return []

    def fetch_similar_ads(self, target: dict, query: dict, limit: int, exclude_urls: set) -> list:
        """Run MongoDB aggregation pipeline to find similar vehicles."""
        try:
            match_clause = {k: v for k, v in query.items() if v is not None}
            if exclude_urls:
                match_clause["url"] = {"$nin": list(exclude_urls)}

            pipeline = [
                {"$match": match_clause},
                {
                    "$addFields": {
                        "distance": {
                            "$add": [
                                {"$abs": {"$subtract": ["$year", target.get("year", 0)]}},
                                {"$divide": [{"$abs": {"$subtract": ["$mileage", target.get("mileage", 0)]}}, 1000]},
                                {"$divide": [{"$abs": {"$subtract": ["$engine_capacity", target.get("engine_capacity", 0)]}}, 100]}
                            ]
                        }
                    }
                },
                {"$sort": {"distance": 1}},
                {"$limit": limit},
                {
                    "$project": {
                        "_id": 0,
                        "image": 1,
                        "title": 1,
                        "year": 1,
                        "mileage": 1,
                        "price": 1,
                        "url": 1,
                        "distance": 1
                    }
                }
            ]
            return list(self.collection.aggregate(pipeline))

        except Exception as e:
            err(f"Failed to fetch similar vehicles from the database. Error: {e}")
            return []


vehicle_data_repo = VehicleDataRepo()
