from bson import ObjectId
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError

from app.db.database import database
from app.utils.logger import err, info, warn


class AdLinks:
    def __init__(self):
        self.collection = None
        self.collection_name = "ad_links"

    def set_collection(self) -> None:
        """Ensures the collection is set before using it."""
        if self.collection is None:
            if database.db is None:
                raise Exception("Database connection is not initialized.")
            self.collection = database.db[self.collection_name]

            # Ensure URLs are globally unique
            self.collection.create_index("url", unique=True)


    def save(self, source: str, urls: list) -> None:
        """Saves multiple URLs for a source. Avoids duplicates globally."""
        if not urls:
            return

        try:
            self.set_collection()

            # Prepare bulk operations
            operations = [
                UpdateOne(
                    {"url": url},
                    {"$setOnInsert": {"url": url, "source": source}},
                    upsert=True
                )
                for url in urls
            ]

            if operations:
                self.collection.bulk_write(operations, ordered=False)

        except BulkWriteError:
            warn("Some URLs already existed, inserted the rest.")
        except Exception as e:
            err(f"Failed to save URLs to the {self.collection_name} database. Error: {e}")


    def get_total_ad_count(self) -> int:
        """Returns the total count of URLs in the collection."""
        try:
            self.set_collection()
            return self.collection.count_documents({})
        except Exception as e:
            err(f"Failed to get total ad count from {self.collection_name}. Error: {e}")
            return 0


    def get_by_source_in_paginated(self, source: str, page: int = 1, page_size: int = 50) -> list:
        """Returns a paginated list of URLs for a given source."""
        try:
            self.set_collection()
            skip_count = (page - 1) * page_size
            cursor = self.collection.find(
                {"source": source},
                {"_id": 1, "url": 1}
            ).skip(skip_count).limit(page_size)

            return [doc for doc in cursor]

        except Exception as e:
            err(f"Failed to get paginated URLs for {source}. Error: {e}")
            return []


    def delete_by_ids(self, ids: list) -> None:
        """Deletes multiple url documents by their _id."""
        try:
            self.set_collection()
            object_ids = [ObjectId(_id) for _id in ids]
            result = self.collection.delete_many({"_id": {"$in": object_ids}})
            info(f"Deleted {result.deleted_count} urls from {self.collection_name}.")
        except Exception as e:
            err(f"Failed to delete urls by ids from {self.collection_name}. Error: {e}")


    def drop(self) -> None:
        """Drops the 'ad_links' collection."""
        try:
            self.set_collection()
            self.collection.drop()
            info("'ad_links' collection dropped.")
        except Exception as e:
            err(f"Failed to drop {self.collection_name} collection. Error: {e}")


ad_links_repo = AdLinks()
