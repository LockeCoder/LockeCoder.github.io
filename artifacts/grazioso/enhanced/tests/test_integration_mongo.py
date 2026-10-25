"""Optional real MongoDB integration test. Run when TEST_MONGO_URI is configured."""
import os
import pytest

if not os.environ.get("TEST_MONGO_URI"):
    pytest.skip("Set TEST_MONGO_URI to run MongoDB integration tests", allow_module_level=True)

from pymongo import MongoClient
from CRUD_Python_Module import AnimalShelter, DataValidationError
from rescue_filters import query_for


def test_real_mongodb_end_to_end():
    client = MongoClient(os.environ["TEST_MONGO_URI"], serverSelectionTimeoutMS=4000)
    db_name = "grazioso_capstone_tests"
    collection = "animals"
    client.drop_database(db_name)
    try:
        repo = AnimalShelter(db_name=db_name, col_name=collection, client=client)
        ids = repo.ensure_indexes()
        assert "rescue_profile_lookup" in ids
        for i, breed in enumerate(["Newfoundland", "Labrador Retriever Mix", "Rottweiler"]):
            assert repo.create({"animal_id": f"TEST-{i}", "name": "Dog", "animal_type": "Dog",
                                "breed": breed, "sex_upon_outcome": "Intact Male", "location_lat": 30.0,
                                "location_long": -97.0})
        page = repo.read_page({}, page=0, page_size=2, projection=["animal_id", "breed"])
        assert page.total == 3 and len(page.documents) == 2
        assert all("_id" not in row for row in page.documents)
        assert repo.read_page({}, page=1, page_size=2).total == 3
        water = repo.read_page(query_for("water"), page_size=10)
        assert water.total == 2
        aggregate = repo.aggregate_breed_distribution({})
        assert sum(row["count"] for row in aggregate) == 3
        assert repo.update({"animal_id": "TEST-0"}, {"$set": {"color": "Black"}}) == 1
        with pytest.raises(DataValidationError):
            repo.delete({})
        assert repo.delete({"animal_id": "TEST-0"}) == 1
        assert repo.read_page({}).total == 2
    finally:
        client.drop_database(db_name)
        client.close()
