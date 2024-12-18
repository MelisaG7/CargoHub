import pytest
import json
import os
from services.item_lines import *
from models.Models import ItemLine

# Sample dummy data for tests
DUMMY_DATA = [
    {"id": 1, "name": "Home Appliances", "description": "",
        "created_at": "1979-01-16 07:07:50", "updated_at": "2024-01-05 23:53:25"},
    {"id": 2, "name": "Office Supplies", "description": "",
        "created_at": "2009-07-18 08:13:40", "updated_at": "2020-01-12 14:32:49"},
    {"id": 3, "name": "Fashion", "description": "",
        "created_at": "1990-01-04 22:40:49", "updated_at": "2003-05-17 08:21:43"}
]

item_lines = ItemLines(".data/", True)


def test_get_item_lines():
    """Test retrieving all item lines from the data."""
    item_lines.data = DUMMY_DATA.copy()
    data = item_lines.get_item_lines()
    assert data == DUMMY_DATA


def test_get_item_line():
    """Test retrieving a specific item line by ID."""
    # item_lines = ItemLines(".data/", True)
    item_lines.data = DUMMY_DATA.copy()
    assert item_lines.get_item_line(2) == DUMMY_DATA[1]
    assert item_lines.get_item_line(999) is None  # Test for non-existing ID


def test_add_item_line():
    """Test adding a new item line."""
    # item_lines = ItemLines(".data/", True)
    item_lines.data = DUMMY_DATA.copy()
    # new_item = {"id": 4, "name": "Electronics", "description": ""}
    new_item = ItemLine(id=4, name="Electronics", description="")
    item_lines.add_item_line(new_item)

    # Check if the item was added
    data = item_lines.get_item_lines()
    assert len(data) == 4
    assert data[-1]["id"] == 4
    assert data[-1]["name"] == "Electronics"
    assert "created_at" in data[-1]
    assert "updated_at" in data[-1]


def test_update_item_line():
    """Test updating an existing item line."""
    # item_lines = ItemLines(".data/", True)
    item_lines.data = DUMMY_DATA.copy()
    # updated_item = {"id": 2, "name": "Updated Office Supplies",
    #                 "description": "Updated description"}
    updated_item = ItemLine(id=2, name="Updated Office Supplies", description="Updated description")

    item_lines.update_item_line(2, updated_item)

    # Check if the item was updated
    data = item_lines.get_item_lines()
    assert data[1]["name"] == "Updated Office Supplies"
    assert data[1]["description"] == "Updated description"
    assert "updated_at" in data[1]


def test_remove_item_line():
    """Test removing an existing item line."""
    # item_lines = ItemLines(".data/", True)
    item_lines.data = DUMMY_DATA.copy()
    amount = len(item_lines.data)

    item_lines.remove_item_line(2)
    updated_amount = len(item_lines.data)
    # Check if the item was removed
    data = item_lines.get_item_lines()
    assert updated_amount == amount - 1
    assert all(item["id"] != 2 for item in data)
