import pytest
from services.inventories import Inventories
from models.Models import Inventory
import fastapi


class TestInventories:

    def setup_method(self):
        self.inventories = Inventories("./data/", True)
        self.inventories.inventory_database = [
            {
                "id": 13,
                "item_id": "P000013",
                "description": "Synergistic secondary utilization",
                "item_reference": "aaB64234x",
                "locations": [
                    9763,
                    26934,
                    26986,
                    29976,
                    30032,
                    21508,
                    19470,
                    19841,
                    14018,
                    617,
                    11413,
                    11455
                ],
                "total_on_hand": 1,
                "total_expected": 1,
                "total_ordered": 1,
                "total_allocated": 1,
                "total_available": 1,
                "created_at": "1990-03-18 02:27:37",
                "updated_at": "2004-01-03 07:09:14"
            },
            {
                "id": 14,
                "item_id": "P000013",
                "description": "I am just a girl",
                "item_reference": "aaB64234x",
                "locations": [
                    9763,
                    26934,
                    26986,
                    29976,
                    30032,
                    21508,
                    19470,
                    19841,
                    14018,
                    617,
                    11413,
                    11455
                ],
                "total_on_hand": 1,
                "total_expected": 1,
                "total_ordered": 1,
                "total_allocated": 1,
                "total_available": 1,
                "created_at": "1990-03-18 02:27:37",
                "updated_at": "2004-01-03 07:09:14"
            }
        ]

    def test_get_inventory(self):
        # The system shall provide the user with information of an inventory
        # object given a valid ID from the user. 
        # Test bestaande ID
        result = self.inventories.get_inventory(13)
        assert result == self.inventories.inventory_database[0]
        # Test Niet bestaande ID
        with pytest.raises(fastapi.HTTPException):
            self.inventories.get_inventory(18)
        # Test string of 
        with pytest.raises(fastapi.HTTPException):
            self.inventories.get_inventory("13")

        with pytest.raises(fastapi.HTTPException):
            self.inventories.get_inventory("dertien")

    def test_get_inventories_for_item(self):
        # The system must provide the user with all inventory objects given
        # a valid item ID from the user. 
        result = self.inventories.get_inventories_for_item("P000013")
        assert result == [self.inventories.inventory_database[0],
                          self.inventories.inventory_database[1]]
        # Thunder/api gebruikt nooit deze methode maar automatisch
        # test_get_inventory(id)

        # test niet bestaande item ID
        result = self.inventories.get_inventories_for_item("P000018")
        assert result == []

    def test_get_items_for_inventory(self):
        # result["total_expected"] += x["total_expected"]
        # result["total_ordered"] += x["total_ordered"]
        # result["total_allocated"] += x["total_allocated"]
        # result["total_available"] += x["total_available"],

        # Wat ik verwacht:
        # result["total_expected"] = 2
        # result["total_orderdered"] = 2
        # result["total_allocated"] = 2
        # result["total_available"] = 2

        result = self.inventories.get_inventory_totals_for_item("P000013")
        assert result["total_expected"] == 2
        assert result["total_ordered"] == 2
        assert result["total_allocated"] == 2
        assert result["total_available"] == 2

    def test_add_inventory(self):
        to_be_added = Inventory(
            id=15,
            item_id="P000015",
            description="fall shoes",
            item_reference="aaB64234x",
            locations=[
                9763,
                26934,
                26986,
                29976,
                30032,
                21508,
                19470,
                19841,
                14018,
                617,
                11413,
                11455
            ],
            total_on_hand=1,
            total_expected=1,
            total_ordered=1,
            total_allocated=1,
            total_available=1,
        )

        self.inventories.add_inventory(to_be_added)
        assert self.inventories.inventory_database.__len__() == 3

    def test_remove_inventory(self):
        self.inventories.remove_inventory(13)
        assert self.inventories.inventory_database.__len__() == 1
        with pytest.raises(fastapi.HTTPException):
            self.inventories.remove_inventory(2)
        assert self.inventories.inventory_database.__len__() == 1

        with pytest.raises(fastapi.HTTPException):
            self.inventories.remove_inventory(-14)
        assert self.inventories.inventory_database.__len__() == 1
        with pytest.raises(fastapi.HTTPException):
            self.inventories.remove_inventory(13)

    # The system shall provide the user the total items of all inventory objects that match the given item ID. 
    # The user must be an admin to request adding an inventory object to the database as well as updating or deleting an object.
    # The system shall add an inventory object given a valid object from a body by an admin user.
    # The system shall update an inventory object in the inventory database given an inventory object with a matching ID. 
    # The system shall delete an inventory object from the inventory database given a valid and existing inventory ID by an admin user.,


if __name__ == '__main__':
    pytest.main()