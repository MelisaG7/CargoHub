from models.item_groups import ItemGroups

'''
{"id": 0,
"name": "Electronics",
"description": "",
'''


class ItemGroupsFoutHandling:

    def __init__(self):
        self.itemgroups = ItemGroups("", True)
        self.RequiredFields = [
            "id", "name", "description"
        ]

    def check_valid_id(self, itemgroup_id):
        # checks on negative ids
        if itemgroup_id < 0:
            return False
        return True

    def check_valid_body(self, itemgroup):
        # checks if all required fields in body
        for field in self.RequiredFields:
            if field not in itemgroup:
                return False
        return True

    def check_get_itemgroup(self, itemgroup_id):
        return self.check_valid_id(itemgroup_id)

    def check_add_itemgroup(self, itemgroup):
        if self.check_valid_body(itemgroup):
            # check if id not in database
            for itemgroep in self.itemgroups.item_groups_database:
                if itemgroep["id"] == itemgroup["id"]:
                    return False
            return True
        return False

    def check_put_itemgroup(self, itemgroup, itemgroup_id):
        if self.check_valid_body(itemgroup):
            # check if itemgroup_id is the same as itemgroup["id"]
            if itemgroup["id"] != itemgroup_id:
                return False
        return True

    def check_remove_itemgroup(self, itemgroup_id):
        return self.check_valid_id(itemgroup_id)
