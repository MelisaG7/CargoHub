import pytest
from models.items import Items

# Sample dummy data for tests
DUMMY_DATA = [
    {"uid": "P000003", "code": "QVm03739H", "description": "Cloned actuating artificial intelligence", "short_description": "we", "upc_code": "3722576017240", "model_number": "aHx-68Q4", "commodity_code": "t-541-F0g", "item_line": 54, "item_group": 88,
        "item_type": 42, "unit_purchase_quantity": 30, "unit_order_quantity": 17, "pack_order_quantity": 11, "supplier_id": 2, "supplier_code": "SUP237", "supplier_part_number": "r-920-z2C", "created_at": "1994-06-02 06:38:40", "updated_at": "1999-10-13 01:10:32"},
    {"uid": "P000004", "code": "zdN19039A", "description": "Pre-emptive asynchronous throughput", "short_description": "take", "upc_code": "9668154959486", "model_number": "pZ-7816", "commodity_code": "IFq-47R1", "item_line": 58, "item_group": 23,
        "item_type": 40, "unit_purchase_quantity": 21, "unit_order_quantity": 20, "pack_order_quantity": 20, "supplier_id": 34, "supplier_code": "SUP140", "supplier_part_number": "T-210-I4M", "created_at": "2005-08-23 00:48:17", "updated_at": "2017-04-29 15:25:25"},
    {"uid": "P000005", "code": "mHo61152n", "description": "Stand-alone 24hour emulation", "short_description": "there", "upc_code": "0943113854446", "model_number": "j-587-L3H", "commodity_code": "67-vxkaB7P", "item_line": 16, "item_group": 50,
        "item_type": 28, "unit_purchase_quantity": 44, "unit_order_quantity": 2, "pack_order_quantity": 20, "supplier_id": 35, "supplier_code": "SUP347", "supplier_part_number": "NzG-36a1", "created_at": "2016-03-28 10:35:32", "updated_at": "2024-05-20 22:42:05"}
]

# Create an instance of Itemsp
items = Items(".data/", True)


def test_get_items():
    """Test retrieving all items from the data."""
    items.data = DUMMY_DATA.copy()
    data = items.get_items()
    assert data == DUMMY_DATA


def test_get_item():
    """Test retrieving a specific item by UID."""
    items.data = DUMMY_DATA.copy()
    assert items.get_item("P000004") == DUMMY_DATA[1]
    assert items.get_item("P999999") is None  # Test for non-existing UID


def test_get_items_for_item_line():
    """Test retrieving items for a specific item line."""
    items.data = DUMMY_DATA.copy()
    result = items.get_items_for_item_line(58)
    assert len(result) == 1
    assert result[0]["uid"] == "P000004"


def test_get_items_for_item_group():
    """Test retrieving items for a specific item group."""
    items.data = DUMMY_DATA.copy()
    result = items.get_items_for_item_group(88)
    assert len(result) == 1
    assert result[0]["uid"] == "P000003"


def test_get_items_for_item_type():
    """Test retrieving items for a specific item type."""
    items.data = DUMMY_DATA.copy()
    result = items.get_items_for_item_type(28)
    assert len(result) == 1
    assert result[0]["uid"] == "P000005"


def test_get_items_for_supplier():
    """Test retrieving items for a specific supplier."""
    items.data = DUMMY_DATA.copy()
    result = items.get_items_for_supplier(35)
    assert len(result) == 1
    assert result[0]["uid"] == "P000005"


def test_add_item():
    """Test adding a new item."""
    items.data = DUMMY_DATA.copy()
    new_item = {"uid": "P000006", "code": "newItem123", "description": "Newly added item", "short_description": "new", "upc_code": "1234567890123", "model_number": "NM-9876", "commodity_code": "NC-123", "item_line": 60,
                "item_group": 30, "item_type": 45, "unit_purchase_quantity": 12, "unit_order_quantity": 10, "pack_order_quantity": 5, "supplier_id": 10, "supplier_code": "SUP567", "supplier_part_number": "SP-001"}

    items.add_item(new_item)

    # Check if the item was added
    data = items.get_items()
    assert len(data) == 4
    assert data[-1]["uid"] == "P000006"
    assert data[-1]["description"] == "Newly added item"
    # assert "created_at" in data[-1]
    # assert "updated_at" in data[-1]


def test_update_item():
    """Test updating an existing item."""
    items.data = DUMMY_DATA.copy()
    updated_item = {"uid": "P000004", "code": "updatedCode", "description": "Updated description", "short_description": "updated", "upc_code": "9999999999999", "model_number": "UP-9999", "commodity_code": "UP-123",
                    "item_line": 58, "item_group": 23, "item_type": 40, "unit_purchase_quantity": 50, "unit_order_quantity": 25, "pack_order_quantity": 20, "supplier_id": 34, "supplier_code": "SUP140", "supplier_part_number": "T-210-I4M"}

    items.update_item("P000004", updated_item)

    # Check if the item was updated
    data = items.get_items()
    assert data[1]["code"] == "updatedCode"
    assert data[1]["description"] == "Updated description"
    assert "updated_at" in data[1]


def test_remove_item():
    """Test removing an existing item."""
    items.data = DUMMY_DATA.copy()
    amount = len(items.data)

    items.remove_item("P000003")

    # Check if the item was removed
    data = items.get_items()
    updated_amount = len(items.data)
    assert updated_amount == amount - 1
    assert all(item["uid"] != "P000003" for item in data)
