import pytest
import sys
import os

from services.locations import Locations

# Mock LOCATIONS data om mee te testen
LOCATIONS = [
    {"id": 1, "name": "Location 1", "warehouse_id": 100},
    {"id": 2, "name": "Location 2", "warehouse_id": 101},
    {"id": 3, "name": "Location 3", "warehouse_id": 100},
]

# de class direct aanroepen en data invoegen

def test_get_locations():
    loc = Locations(root_path="", is_debug=True)
    loc.data = LOCATIONS  # Mock data invoegen
    assert loc.get_locations() == LOCATIONS  # Controleer of we de juiste locaties krijgen

def test_get_location():
    loc = Locations(root_path="", is_debug=True)
    loc.data = LOCATIONS
    assert loc.get_location(1) == LOCATIONS[0]  # Locatie 1 ophalen
    assert loc.get_location(999) is None  # Niet-bestaande locatie moet None retourneren

def test_get_locations_in_warehouse():
    loc = Locations(root_path="", is_debug=True)
    loc.data = LOCATIONS
    result = loc.get_locations_in_warehouse(100)
    assert result == [LOCATIONS[0], LOCATIONS[2]]  # Twee locaties in warehouse_id 100

def test_remove_location():
    loc = Locations(root_path="", is_debug=True)
    loc.data = LOCATIONS.copy()
    loc.remove_location(1)
    assert len(loc.data) == 2  # Controleer of de locatie is verwijderd
    assert all(x["id"] != 1 for x in loc.data)  # Controleer of geen locatie met id 1 meer bestaat
