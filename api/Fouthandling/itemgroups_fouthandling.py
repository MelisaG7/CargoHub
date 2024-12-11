from models.Models import ItemGroup


'''
{"id": 0,
"name": "Electronics",
"description": "",
'''


class ItemGroupsFoutHandling:

    def itemgroups(self):
        from services.item_groups import ItemGroups
        return ItemGroups("./data/", False)

    def check_valid_id(self, itemgroup_id):
        # checks on negative ids
        if itemgroup_id < 0:
            return False
        return True

    def check_get_itemgroup(self, itemgroup_id: int):
        return self.check_valid_id(itemgroup_id)

    def check_add_itemgroup(self, itemgroup: ItemGroup):
        # check if id not in database
        for itemgroep in self.itemgroups().item_groups_database:
            if itemgroep["id"] == itemgroup.model_dump()["id"]:
                return False
        return True

    def check_put_itemgroup(self, itemgroup: ItemGroup, itemgroup_id: int):
        if itemgroup.model_dump()["id"] != itemgroup_id:
            return False
        return True

    def check_remove_itemgroup(self, itemgroup_id: int):
        return self.check_valid_id(itemgroup_id)
