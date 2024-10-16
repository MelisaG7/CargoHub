import pytest
import json
from models.item_types import *

# Sample dummy data for tests
DUMMY_DATA = [
    {"id": 1, "name": "Desktop", "description": "", "created_at": "1993-07-28 13:43:32", "updated_at": "2022-05-12 08:54:35"},
    {"id": 2, "name": "Tablet", "description": "", "created_at": "1977-05-01 00:05:04", "updated_at": "2001-04-14 02:41:59"},
    {"id": 3, "name": "Smartphone", "description": "", "created_at": "2014-08-23 03:26:57", "updated_at": "2017-09-20 11:51:15"}
]

# Create an instance of ItemTypes
item_types = ItemTypes(".data/", True)

def test_get_item_types():
    """Test retrieving all item types from the data."""
    item_types.data = DUMMY_DATA
    data = item_types.get_item_types()
    assert data == DUMMY_DATA

def test_get_item_type():
    """Test retrieving a specific item type by ID."""
    item_types.data = DUMMY_DATA
    assert item_types.get_item_type(2) == DUMMY_DATA[1]
    assert item_types.get_item_type(999) is None  # Test for non-existing ID

def test_add_item_type():
    """Test adding a new item type."""
    item_types.data = DUMMY_DATA
    new_item = {"id": 4, "name": "Laptop", "description": ""}
    item_types.add_item_type(new_item)

    # Check if the item was added
    data = item_types.get_item_types()
    assert len(data) == 4
    assert data[-1]["id"] == 4
    assert data[-1]["name"] == "Laptop"
    assert "created_at" in data[-1]
    assert "updated_at" in data[-1]

def test_update_item_type():
    """Test updating an existing item type."""
    item_types.data = DUMMY_DATA
    updated_item = {"id": 2, "name": "Updated Tablet", "description": "Updated description"}
    item_types.update_item_type(2, updated_item)

    # Check if the item was updated
    data = item_types.get_item_types()
    assert data[1]["name"] == "Updated Tablet"
    assert data[1]["description"] == "Updated description"
    assert "updated_at" in data[1]

def test_remove_item_type():
    """Test removing an existing item type."""
    item_types.data = DUMMY_DATA

    item_types.remove_item_type(2)

    # Check if the item was removed
    data = item_types.get_item_types()
    print(data)

    assert len(data) == 2
    assert all(item["id"] != 2 for item in data)
