"""Validated MongoDB data access for the Grazioso Salvare rescue dashboard.

CS 499 database enhancement: indexes, projected/filtered server-side pagination,
aggregation, environment configuration, safer writes and explicit error handling.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence
from urllib.parse import quote_plus

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError


class DataValidationError(ValueError):
    """A caller supplied an invalid filter, field, or operation."""


class DataAccessError(RuntimeError):
    """MongoDB could not complete an operation (distinct from zero matches)."""


# Known Austin Animal Center import columns. Unknown fields/operators are rejected.
ALLOWED_FIELDS = frozenset({
    "age_upon_outcome", "animal_id", "animal_type", "breed", "color",
    "date_of_birth", "datetime", "monthyear", "name", "outcome_subtype",
    "outcome_type", "sex_upon_outcome", "location_lat", "location_long",
    "age_upon_outcome_in_weeks",
})
ALLOWED_COMPARISONS = frozenset({"$eq", "$ne", "$gte", "$lte", "$gt", "$lt", "$in", "$nin"})
ALLOWED_LOGICAL = frozenset({"$and", "$or"})
MAX_PAGE_SIZE = 100


@dataclass(frozen=True)
class PageResult:
    documents: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int


def _check_field(field: Any) -> str:
    if not isinstance(field, str) or field not in ALLOWED_FIELDS:
        raise DataValidationError(f"Unsupported database field: {field!r}")
    return field


def _validate_filter(query: Mapping[str, Any], *, allow_empty: bool = True) -> Dict[str, Any]:
    if not isinstance(query, dict):
        raise DataValidationError("A database filter must be a dictionary")
    if not query and not allow_empty:
        raise DataValidationError("Write operations require a nonempty filter")
    validated = {}
    for key, value in query.items():
        if key in ALLOWED_LOGICAL:
            if not isinstance(value, list) or not value:
                raise DataValidationError(f"{key} requires a nonempty list of filters")
            validated[key] = [_validate_filter(part, allow_empty=False) for part in value]
            continue
        _check_field(key)
        if isinstance(value, dict):
            if not value:
                raise DataValidationError("Comparison operator dictionary cannot be empty")
            operators = {}
            for operator, operand in value.items():
                if operator not in ALLOWED_COMPARISONS:
                    raise DataValidationError(f"Unsupported query operator: {operator!r}")
                if operator in {"$in", "$nin"}:
                    if not isinstance(operand, (list, tuple)) or not operand or len(operand) > 100:
                        raise DataValidationError(f"{operator} requires 1–100 values")
                    if any(isinstance(v, (dict, list, tuple)) for v in operand):
                        raise DataValidationError("Nested query values are not permitted")
                    operand = list(operand)
                elif isinstance(operand, (dict, list, tuple)):
                    raise DataValidationError("Nested query values are not permitted")
                operators[operator] = operand
            validated[key] = operators
        elif isinstance(value, (list, tuple)):
            raise DataValidationError("Lists must be supplied using $in or $nin")
        else:
            validated[key] = value
    return validated


def _validate_projection(projection: Optional[Sequence[str]]) -> Dict[str, int]:
    if projection is None:
        fields = list(sorted(ALLOWED_FIELDS))
    elif isinstance(projection, (str, bytes)) or not isinstance(projection, (list, tuple)):
        raise DataValidationError("Projection must be a list of approved field names")
    else:
        fields = [_check_field(field) for field in projection]
        if not fields:
            raise DataValidationError("Projection must contain at least one field")
    return {**{field: 1 for field in fields}, "_id": 0}


def _validate_update(values: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    if not isinstance(values, dict) or not values:
        raise DataValidationError("Update must be a nonempty dictionary")
    if set(values) - {"$set", "$unset"}:
        raise DataValidationError("Only $set and $unset updates are supported")
    normalized = {}
    for operator, mapping in values.items():
        if not isinstance(mapping, dict) or not mapping:
            raise DataValidationError(f"{operator} requires a nonempty field dictionary")
        normalized[operator] = {_check_field(field): val for field, val in mapping.items()}
        if any(isinstance(value, dict) and any(str(k).startswith("$") for k in value)
               for value in mapping.values()):
            raise DataValidationError("Nested update operators are not permitted")
    return normalized


def _clean_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB documents into dashboard-friendly JSON-compatible rows."""
    cleaned = {}
    for key, value in document.items():
        if key == "_id":
            continue
        if hasattr(value, "isoformat"):
            value = value.isoformat()
        cleaned[key] = value
    return cleaned


class AnimalShelter:
    """MongoDB repository with validated CRUD, paging, indexes and aggregation."""

    def __init__(self, username: str = "", password: str = "", host: str = "localhost",
                 port: int = 27017, db_name: str = "aac", col_name: str = "animals",
                 server_timeout_ms: int = 5000, auth_source: str = "admin",
                 *, mongo_uri: Optional[str] = None, client: Any = None):
        if (bool(username) != bool(password)) and not mongo_uri and client is None:
            raise DataValidationError("Supply both MongoDB username and password, or neither")
        if client is not None:
            self.client = client
        elif mongo_uri:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=server_timeout_ms)
        elif username and password:
            uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}:{port}"
            self.client = MongoClient(uri, authSource=auth_source,
                                      serverSelectionTimeoutMS=server_timeout_ms)
        else:
            self.client = MongoClient(f"mongodb://{host}:{port}",
                                      serverSelectionTimeoutMS=server_timeout_ms)
        self.database = self.client[db_name]
        self.collection = self.database[col_name]
        try:
            self.client.admin.command("ping")
        except PyMongoError as exc:
            # Do not echo exception strings: driver errors may include connection URIs.
            raise DataAccessError("MongoDB connection or authentication failed") from exc

    @classmethod
    def from_env(cls, *, client: Any = None) -> "AnimalShelter":
        """Read connection settings at startup; no passwords embedded in code."""
        uri = os.getenv("MONGO_URI", "").strip()
        username = os.getenv("MONGO_USERNAME", "").strip()
        password = os.getenv("MONGO_PASSWORD", "")
        if not uri and bool(username) != bool(password):
            raise DataValidationError("Set both MONGO_USERNAME and MONGO_PASSWORD")
        try:
            port = int(os.getenv("MONGO_PORT", "27017"))
            timeout = int(os.getenv("MONGO_TIMEOUT_MS", "5000"))
        except ValueError as exc:
            raise DataValidationError("MONGO_PORT and MONGO_TIMEOUT_MS must be integers") from exc
        if not (1 <= port <= 65535) or not (100 <= timeout <= 120000):
            raise DataValidationError("MongoDB port or timeout is outside supported limits")
        return cls(username=username, password=password, host=os.getenv("MONGO_HOST", "localhost"),
                   port=port, db_name=os.getenv("MONGO_DB", "aac"),
                   col_name=os.getenv("MONGO_COLLECTION", "animals"),
                   auth_source=os.getenv("MONGO_AUTH_SOURCE", "admin"),
                   server_timeout_ms=timeout, mongo_uri=uri or None, client=client)

    def create(self, data: Mapping[str, Any]) -> bool:
        if not isinstance(data, dict) or not data:
            raise DataValidationError("Create requires a nonempty document dictionary")
        for field in data:
            _check_field(field)
        try:
            return bool(self.collection.insert_one(dict(data)).inserted_id)
        except PyMongoError as exc:
            raise DataAccessError("Failed to insert animal record") from exc

    def read(self, query: Mapping[str, Any]) -> List[Dict[str, Any]]:
        """Compatibility API: for large result sets use read_page() instead."""
        validated = _validate_filter(query)
        try:
            return [_clean_document(doc) for doc in self.collection.find(validated, {"_id": 0})]
        except PyMongoError as exc:
            raise DataAccessError("Failed to retrieve animal records") from exc

    def read_page(self, query: Mapping[str, Any], *, page: int = 0, page_size: int = 10,
                  sort_field: str = "animal_id", sort_direction: int = ASCENDING,
                  projection: Optional[Sequence[str]] = None) -> PageResult:
        """MongoDB executes filtering, projection, sorting, skip and limit."""
        validated = _validate_filter(query)
        if type(page) is not int or page < 0:
            raise DataValidationError("Page must be a nonnegative integer")
        if type(page_size) is not int or not 1 <= page_size <= MAX_PAGE_SIZE:
            raise DataValidationError(f"Page size must be between 1 and {MAX_PAGE_SIZE}")
        _check_field(sort_field)
        if sort_direction not in (ASCENDING, DESCENDING):
            raise DataValidationError("Sort direction must be 1 or -1")
        fields = _validate_projection(projection)
        # Secondary key stabilizes pagination when primary sort values repeat.
        order = [(sort_field, sort_direction)]
        if sort_field != "animal_id":
            order.append(("animal_id", ASCENDING))
        order.append(("_id", ASCENDING))
        try:
            total = self.collection.count_documents(validated)
            cursor = self.collection.find(validated, fields).sort(order).skip(page * page_size).limit(page_size)
            return PageResult([_clean_document(doc) for doc in cursor], total, page, page_size)
        except PyMongoError as exc:
            raise DataAccessError("Failed to retrieve paginated animal records") from exc

    def aggregate_breed_distribution(self, query: Mapping[str, Any], *, limit: int = 12) -> List[Dict[str, Any]]:
        """Calculate breed counts in MongoDB across all matching records, not one UI page."""
        validated = _validate_filter(query)
        if type(limit) is not int or not 1 <= limit <= 100:
            raise DataValidationError("Aggregation limit must be between 1 and 100")
        pipeline = [
            {"$match": validated},
            {"$group": {"_id": {"$ifNull": ["$breed", "Unknown"]}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1, "_id": 1}},
            {"$limit": limit},
        ]
        try:
            return [{"breed": str(doc["_id"]), "count": int(doc["count"])}
                    for doc in self.collection.aggregate(pipeline)]
        except PyMongoError as exc:
            raise DataAccessError("Failed to aggregate breed distribution") from exc

    def ensure_indexes(self) -> List[str]:
        """Create indexes aligned to the rescue filters and stable course listing."""
        definitions = [
            ([('animal_type', ASCENDING), ('sex_upon_outcome', ASCENDING),
              ('breed', ASCENDING), ('age_upon_outcome_in_weeks', ASCENDING)], 'rescue_profile_lookup'),
            ([('animal_id', ASCENDING)], 'animal_id_lookup'),
        ]
        try:
            return [self.collection.create_index(fields, name=name) for fields, name in definitions]
        except PyMongoError as exc:
            raise DataAccessError("Failed to create rescue search indexes") from exc

    def update(self, filter: Mapping[str, Any], new_values: Mapping[str, Any]) -> int:
        validated = _validate_filter(filter, allow_empty=False)
        updates = _validate_update(new_values)
        try:
            return int(self.collection.update_many(validated, updates).modified_count)
        except PyMongoError as exc:
            raise DataAccessError("Failed to update animal records") from exc

    def delete(self, filter: Mapping[str, Any]) -> int:
        validated = _validate_filter(filter, allow_empty=False)
        try:
            return int(self.collection.delete_many(validated).deleted_count)
        except PyMongoError as exc:
            raise DataAccessError("Failed to delete animal records") from exc
