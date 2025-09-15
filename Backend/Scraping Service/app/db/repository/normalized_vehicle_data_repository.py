from bson import ObjectId
from statistics import median
from collections import Counter, defaultdict

from app.db.database import database
from app.utils.logger import err, info


class NormalizedVehicles:
    def __init__(self):
        self.collection = None
        self.collection_name = "normalized_vehicle_data"

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

    def get_stats(self) -> dict:
        """Returns median mileage by year, mode engine capacity and transmission by make, """
        self.set_collection()
        median_mileage_by_year = {}
        mode_engine_capacity_by_make = {}
        mode_transmission_by_make = {}

        try:
            mileage_by_year_pipeline = [
                {"$match": {"year": {"$type": "int"}, "mileage": {"$type": "int"}}},
                {"$group": {
                    "_id": "$year",
                    "mileages": {"$push": "$mileage"}
                }}
            ]
            result = self.collection.aggregate(mileage_by_year_pipeline)
            median_mileage_by_year = {
                str(doc["_id"]): int(median(doc["mileages"]))
                for doc in result if doc["mileages"]
            }
        except Exception as e:
            err(f"Failed to compute median mileage by year. Error: {e}")

        try:
            engine_capacity_by_make_pipeline = [
                {"$match": {"make": {"$type": "string"}, "engine_capacity": {"$type": "int"}}},
                {"$group": {
                    "_id": "$make",
                    "capacities": {"$push": "$engine_capacity"}
                }}
            ]
            result = self.collection.aggregate(engine_capacity_by_make_pipeline)
            mode_engine_capacity_by_make = {
                doc["_id"].strip().title(): Counter(doc["capacities"]).most_common(1)[0][0]
                for doc in result if doc["capacities"]
            }
        except Exception as e:
            err(f"Failed to compute mode engine capacity by make. Error: {e}")

        try:
            transmission_by_make_pipeline = [
                {"$match": {"make": {"$type": "string"}, "transmission": {"$type": "string"}}},
                {"$group": {
                    "_id": "$make",
                    "transmissions": {"$push": "$transmission"}
                }}
            ]
            result = self.collection.aggregate(transmission_by_make_pipeline)
            mode_transmission_by_make = {
                doc["_id"].strip().title(): Counter(doc["transmissions"]).most_common(1)[0][0]
                for doc in result if doc["transmissions"]
            }
        except Exception as e:
            err(f"Failed to compute mode transmission by make. Error: {e}")

        return {
            "median_mileage_by_year": median_mileage_by_year,
            "mode_engine_capacity_by_make": mode_engine_capacity_by_make,
            "mode_transmission_by_make": mode_transmission_by_make
        }

    def get_make_model_frequencies(self) -> dict:
        """
        Returns make-wise unique models with frequencies.
        Structure:
        {
            "Toyota": [{"model": "Land Cruiser Prado", "frequency": 28}, ...],
            "Honda": [{"model": "Civic", "frequency": 15}, ...]
        }
        """
        self.set_collection()

        pipeline = [
            # Only consider documents with non-null make and model
            {"$match": {"make": {"$type": "string"}, "model": {"$type": "string"}}},
            # Group by make and model to count frequency
            {"$group": {
                "_id": {"make": "$make", "model": "$model"},
                "frequency": {"$sum": 1}
            }},
            # Sort by frequency descending
            {"$sort": {"_id.make": 1, "frequency": -1}}
        ]

        result = self.collection.aggregate(pipeline)
        make_model_freq = defaultdict(list)

        for doc in result:
            make = doc["_id"]["make"]
            model = doc["_id"]["model"]
            frequency = doc.get("frequency", 1)
            make_model_freq[make].append({"model": model, "frequency": frequency})

        return dict(make_model_freq)

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


normalized_vehicle_data_repo = NormalizedVehicles()
