"""Named and testable rescue-profile MongoDB filters for Grazioso Salvare."""
from __future__ import annotations

PROFILES = {
    "water": {
        "animal_type": "Dog",
        "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
        "sex_upon_outcome": "Intact Male",
    },
    "mountain": {
        "animal_type": "Dog",
        "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog",
                          "Siberian Husky", "Rottweiler"]},
        "sex_upon_outcome": "Intact Male",
    },
    "disaster": {
        "animal_type": "Dog",
        "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever",
                          "Bloodhound", "Rottweiler"]},
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300},
    },
}


def query_for(option: str) -> dict:
    """Return a fresh filter dictionary; reset and unrecognized values show all."""
    import copy
    return copy.deepcopy(PROFILES.get(option, {}))


def valid_coordinates(record: dict) -> tuple[float, float] | None:
    """Only numeric, finite, geographic coordinates can produce map markers."""
    import math
    try:
        lat = float(record["location_lat"])
        lon = float(record["location_long"])
    except (TypeError, ValueError, KeyError):
        return None
    if not (math.isfinite(lat) and math.isfinite(lon)):
        return None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    return (lat, lon)
