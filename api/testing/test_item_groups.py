import pytest
from services.item_groups import ItemGroups
from fastapi import HTTPException
from models.Models import ItemGroup


class TestItemGroups:

    def setup_method(self):
        self.item_groups = ItemGroups("./data/", is_debug=True)
        self.item_groups.item_groups_database = [ 
            {
                "id": 0,
                "name": "Electronics",
                "description": "",
                "created_at": "1998-05-15 19:52:53",
                "updated_at": "2000-11-20 08:37:56"
            },
            {
                "id": 1,
                "name": "Furniture",
                "description": "",
                "created_at": "2019-09-22 15:51:07",
                "updated_at": "2022-05-18 13:49:28"
            }
        ]

    def test_get_item_groups(self):
        result = self.item_groups.get_item_group(1)
        assert result == self.item_groups.item_groups_database[1]
        with pytest.raises(HTTPException):
            self.item_groups.get_item_group(20)
        with pytest.raises(HTTPException):
            self.item_groups.get_item_group(-1)

    def test_add_item_group(self):
        correct_body = ItemGroup(
            id=2, 
            name="Christian Louboutins",
            description="designer"
        )
        self.item_groups.add_item_group(correct_body)
        assert self.item_groups.item_groups_database.__len__() == 3

    def test_update_item_group(self):
        New_item = ItemGroup(
            id=1,
            name="Heels",
            description="Mango cherry red heels"
        )
        self.item_groups.update_item_group(1, New_item)
        assert self.item_groups.item_groups_database[1]["name"] == "Heels"
        self.item_groups.add_item_group(ItemGroup(id=2, name="Other heels", description="Kitty heels"))
        with pytest.raises(HTTPException):
            self.item_groups.update_item_group(2, ItemGroup(id=1, name="ballerina's", description="flats"))
        # Zou niet moeten lukken want ID bestaat al in de data base namelijk 1
        assert self.item_groups.item_groups_database[2]["id"] == 2

    def test_remove_item_group(self):
        self.item_groups.remove_item_group(1)
        assert self.item_groups.item_groups_database.__len__() == 1


if __name__ == '__main__':
    pytest.main()
