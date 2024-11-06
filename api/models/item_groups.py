import json

from models.base import Base

ITEM_GROUPS = []

# CHANGES:
# Changed 'self.data' to 'self.item_groups_database'
# Changed 'self.data_path' to 'self.item_groups_database_path'
# Changed 'x' and 'i' to 'item_group'


class ItemGroups(Base):
    def __init__(self, root_path, is_debug=False):
        self.item_groups_database_path = root_path + "item_groups.json"
        self.load(is_debug)

    def get_item_groups(self):
        # returns all item_group objects in the database
        return self.item_groups_database

    def get_item_group(self, item_group_id):
        for item_group in self.item_groups_database:
            # The method searches through the database for an item_group object that has the same id as the passed id.
            if item_group["id"] == item_group_id:
                # if there is a match, the found inventory object gets fetched
                return item_group
            # If nothing was found, it returns 'None' and a 200 status_code. The user sees 'null'
        return None

    def add_item_group(self, item_group):
        # This method adds/replaces the values of 'created_at' and 'updated_at' of the passed object to the current date and time
        item_group["created_at"] = self.get_timestamp()
        item_group["updated_at"] = self.get_timestamp()
        # Then the object gets added to the database
        self.item_groups_database.append(item_group)

    def update_item_group(self, item_group_id, item_group):
        # This method changes the value of "updated_at" of the passed item_group object
        item_group["updated_at"] = self.get_timestamp()
        for item_group in range(len(self.item_groups_database)):
            # Then it searches through the database to an object that has the same id as the one passed
            if self.item_groups_database[item_group]["id"] == item_group_id:
                # Then it changes the found object to the one passed as a parameter
                self.item_groups_database[item_group] = item_group
                break

    def remove_item_group(self, item_group_id):
        # This method searches through the database for an object that has the same id as the one passed
        for item_group in self.item_groups_database:
            if item_group["id"] == item_group_id:
                # If there is a match, the found object gets removed from the database
                self.item_groups_database.remove(x)

    def load(self, is_debug):
        if is_debug:
            self.item_groups_database = ITEM_GROUPS
        else:
            f = open(self.item_groups_database_path, "r")
            self.item_groups_database = json.load(f)
            f.close()

    def save(self):
        f = open(self.item_groups_database_path, "w")
        json.dump(self.item_groups_database, f)
        f.close()
