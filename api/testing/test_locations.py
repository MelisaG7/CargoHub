import pytest
import sys
import os

from api.models.locations import Locations

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

def test_add_location():
    loc = Locations(root_path="", is_debug=True)
    loc.data = LOCATIONS.copy()
    new_location = {"id": 4, "name": "Location 4", "warehouse_id": 102}
    loc.add_location(new_location)
    assert len(loc.data) == 4  # Controleer of de nieuwe locatie is toegevoegd
    assert loc.data[-1]["id"] == 4  # De laatste locatie moet de nieuwe locatie zijn

def test_update_location():
    loc = Locations(root_path="", is_debug=True)
    loc.data = LOCATIONS.copy()
    updated_location = {"id": 1, "name": "Updated Location", "warehouse_id": 100}
    loc.update_location(1, updated_location)
    assert loc.data[0]["name"] == "Updated Location"  # Locatie moet zijn bijgewerkt

def test_remove_location():
    loc = Locations(root_path="", is_debug=True)
    loc.data = LOCATIONS.copy()
    loc.remove_location(1)
    assert len(loc.data) == 2  # Controleer of de locatie is verwijderd
    assert all(x["id"] != 1 for x in loc.data)  # Controleer of geen locatie met id 1 meer bestaat
