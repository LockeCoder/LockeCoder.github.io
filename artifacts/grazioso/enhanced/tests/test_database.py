"""Offline unit tests of DB calls, read/write validation, and aggregations."""
import os
import pytest
from unittest.mock import MagicMock

from CRUD_Python_Module import (
    AnimalShelter, DataAccessError, DataValidationError,
    _validate_filter, _validate_projection,
)
from rescue_filters import query_for, valid_coordinates
from pymongo.errors import PyMongoError


@pytest.fixture
def repo():
    client = MagicMock()
    collection = client.__getitem__.return_value.__getitem__.return_value
    return AnimalShelter(client=client), collection, client


def test_connection_health_check(repo):
    _, _, client = repo
    client.admin.command.assert_called_once_with("ping")


def test_reject_partial_credentials():
    with pytest.raises(DataValidationError):
        AnimalShelter(username="admin", password="")


def test_env_reads_settings(monkeypatch):
    for key in ("MONGO_URI", "MONGO_USERNAME", "MONGO_PASSWORD", "MONGO_PORT"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("MONGO_DB", "rescues")
    client = MagicMock()
    r = AnimalShelter.from_env(client=client)
    assert r.database is client["rescues"]


def test_env_rejects_invalid_port(monkeypatch):
    monkeypatch.setenv("MONGO_PORT", "invalid")
    with pytest.raises(DataValidationError):
        AnimalShelter.from_env(client=MagicMock())


def test_filter_rejects_js_style_operator_injection():
    with pytest.raises(DataValidationError):
        _validate_filter({"breed": {"$where": "true"}})
    with pytest.raises(DataValidationError):
        _validate_filter({"$where": "true"})
    with pytest.raises(DataValidationError):
        _validate_filter({"breed": {"$in": []}})


def test_filter_allows_rescue_profiles():
    for name in ("water", "mountain", "disaster", "reset"):
        assert _validate_filter(query_for(name)) == query_for(name)


def test_filter_copy_prevents_profile_mutation():
    water = query_for("water")
    water["breed"]["$in"].clear()
    assert query_for("water")["breed"]["$in"]


def test_projection_is_whitelisted():
    assert _validate_projection(["animal_id", "breed"]) == {"animal_id": 1, "breed": 1, "_id": 0}
    with pytest.raises(DataValidationError):
        _validate_projection(["$password"])


def test_create_validates_and_returns_success(repo):
    r, collection, _ = repo
    collection.insert_one.return_value.inserted_id = "id"
    assert r.create({"animal_id": "A01", "breed": "Husky"}) is True
    collection.insert_one.assert_called_once()
    with pytest.raises(DataValidationError):
        r.create({"$bad": "x"})


def test_read_empty_result_is_not_error(repo):
    r, collection, _ = repo
    collection.find.return_value = iter([])
    assert r.read({}) == []


def test_read_database_error_is_distinct(repo):
    r, collection, _ = repo
    collection.find.side_effect = PyMongoError("database unavailable")
    with pytest.raises(DataAccessError):
        r.read({})


def test_paginate_runs_count_projection_sort_skip_limit_in_mongo(repo):
    r, collection, _ = repo
    collection.count_documents.return_value = 23
    collection.find.return_value.sort.return_value.skip.return_value.limit.return_value = [
        {"animal_id": "A11", "breed": "Husky"}]
    result = r.read_page(query_for("water"), page=2, page_size=10,
                         sort_field="breed", sort_direction=-1,
                         projection=["animal_id", "breed"])
    assert result.total == 23
    assert result.page == 2 and result.page_size == 10
    assert result.documents[0]["animal_id"] == "A11"
    collection.find.assert_called_once_with(query_for("water"),
                                             {"animal_id": 1, "breed": 1, "_id": 0})
    collection.find.return_value.sort.assert_called_once_with([
        ("breed", -1), ("animal_id", 1), ("_id", 1)])
    collection.find.return_value.sort.return_value.skip.assert_called_once_with(20)
    collection.find.return_value.sort.return_value.skip.return_value.limit.assert_called_once_with(10)


@pytest.mark.parametrize("kwargs", [
    {"page": -1}, {"page": True}, {"page_size": 0},
    {"page_size": 101}, {"page_size": 2.5},
    {"sort_field": "__dict__"}, {"sort_direction": 0},
])
def test_invalid_pagination_rejected_before_database_access(repo, kwargs):
    r, collection, _ = repo
    with pytest.raises(DataValidationError):
        r.read_page({}, **kwargs)
    collection.find.assert_not_called()


def test_aggregate_executes_mongo_pipeline(repo):
    r, collection, _ = repo
    collection.aggregate.return_value = [{"_id": "Husky", "count": 9}]
    assert r.aggregate_breed_distribution(query_for("mountain")) == [{"breed": "Husky", "count": 9}]
    pipeline = collection.aggregate.call_args.args[0]
    assert pipeline[0] == {"$match": query_for("mountain")}
    assert "$group" in pipeline[1]
    assert pipeline[2]["$sort"] == {"count": -1, "_id": 1}
    assert pipeline[3] == {"$limit": 12}


def test_indexes_cover_rescue_fields(repo):
    r, collection, _ = repo
    r.ensure_indexes()
    names = [call.kwargs["name"] for call in collection.create_index.call_args_list]
    assert names == ["rescue_profile_lookup", "animal_id_lookup"]


def test_update_requires_nonempty_filter_and_safe_operator(repo):
    r, collection, _ = repo
    with pytest.raises(DataValidationError):
        r.update({}, {"$set": {"breed": "X"}})
    with pytest.raises(DataValidationError):
        r.update({"animal_id": "A"}, {"$inc": {"age_upon_outcome_in_weeks": 1}})
    with pytest.raises(DataValidationError):
        r.update({"animal_id": "A"}, {"$set": {"unknown_field": "X"}})
    collection.update_many.assert_not_called()


def test_update_reports_modified_count(repo):
    r, collection, _ = repo
    collection.update_many.return_value.modified_count = 2
    assert r.update({"breed": "Husky"}, {"$set": {"color": "Black"}}) == 2


def test_delete_requires_nonempty_filter(repo):
    r, collection, _ = repo
    with pytest.raises(DataValidationError):
        r.delete({})
    collection.delete_many.assert_not_called()


def test_delete_reports_actual_deleted_count(repo):
    r, collection, _ = repo
    collection.delete_many.return_value.deleted_count = 2
    assert r.delete({"animal_id": "A"}) == 2


@pytest.mark.parametrize("row", [
    {}, {"location_lat": None, "location_long": -97},
    {"location_lat": "NaN", "location_long": -97},
    {"location_lat": 100, "location_long": -97},
    {"location_lat": 30, "location_long": -200},
])
def test_bad_coordinates_do_not_place_marker(row):
    assert valid_coordinates(row) is None


def test_good_coordinates():
    assert valid_coordinates({"location_lat": "30.5", "location_long": "-97.25"}) == (30.5, -97.25)
