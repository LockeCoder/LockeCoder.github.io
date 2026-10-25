# CRUD_Python_Module.py

from typing import Dict, List
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError


class AnimalShelter:
    """
    CRUD operations for the 'animals' collection in the 'aac' database.

    Public API:
        create(data) -> bool
        read(query) -> list
        update(filter, new_values) -> int
        delete(filter) -> int
    """

    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 27017,
        db_name: str = "aac",
        col_name: str = "animals",
        server_timeout_ms: int = 5000,
        auth_source: str = "admin",
    ):
        """
        Initialize a MongoDB connection.

        If username and password are provided, connect with authentication.
        Otherwise, connect without authentication for local lab environments
        where MongoDB access control is not enabled.
        """
        if username and password:
            encoded_username = quote_plus(username)
            encoded_password = quote_plus(password)
            uri = f"mongodb://{encoded_username}:{encoded_password}@{host}:{port}"

            self.client = MongoClient(
                uri,
                authSource=auth_source,
                serverSelectionTimeoutMS=server_timeout_ms,
            )
        else:
            self.client = MongoClient(
                f"mongodb://{host}:{port}",
                serverSelectionTimeoutMS=server_timeout_ms,
            )

        self.database = self.client[db_name]
        self.collection = self.database[col_name]

        # Health check so bad credentials or connection issues fail early.
        try:
            self.client.admin.command("ping")
        except ServerSelectionTimeoutError as error:
            raise RuntimeError(
                f"Cannot reach MongoDB at {host}:{port}: {error}"
            ) from error
        except PyMongoError as error:
            raise RuntimeError(
                f"MongoDB authentication or connection failed: {error}"
            ) from error

    def create(self, data: Dict) -> bool:
        """
        Insert one document.

        Returns:
            True if the insert succeeds, otherwise False.
        """
        if not isinstance(data, dict) or not data:
            return False

        try:
            result = self.collection.insert_one(data)
            return bool(result.inserted_id)
        except PyMongoError:
            return False

    def read(self, query: Dict) -> List[Dict]:
        """
        Return documents matching the query.

        The MongoDB '_id' field is excluded from returned documents so the
        results work cleanly with the dashboard.
        """
        if not isinstance(query, dict):
            return []

        try:
            cursor = self.collection.find(query, {"_id": 0})
            return list(cursor)
        except PyMongoError:
            return []

    def update(self, filter: Dict, new_values: Dict) -> int:
        """
        Update documents matching the filter.

        new_values should include the MongoDB update operator, such as:
            {"$set": {"animal_type": "Dog"}}

        Returns:
            Number of modified documents, or 0 on error.
        """
        if not isinstance(filter, dict) or not isinstance(new_values, dict):
            return 0

        try:
            result = self.collection.update_many(filter, new_values)
            return int(result.modified_count)
        except PyMongoError:
            return 0

    def delete(self, filter: Dict) -> int:
        """
        Delete documents matching the filter.

        Returns:
            Number of deleted documents, or 0 on error.
        """
        if not isinstance(filter, dict):
            return 0

        try:
            result = self.collection.delete_many(filter)
            return int(result.deleted_count)
        except PyMongoError:
            return 0
