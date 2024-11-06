import json

from models.base import Base

INVENTORIES = []

'''
CHANGES:
Changed 'self.data' to 'self.inventory_database'
Changed 'self.data_path' to 'self.inventory_database_path'
Changed 'x' and 'i' to 'inventory'
Changed 'result' to 'found_inventories' (get_inventories_for_item)
Changed 'result' to 'inventory_totals' (get_inventory_totals_for_item)
'''


class Inventories(Base):
    def __init__(self, root_path, is_debug=False):
        self.inventory_database_path = root_path + "inventories.json"
        self.load(is_debug)

    def get_inventories(self):
        # This method returns all inventory objects in the database
        return self.inventory_database

    def get_inventory(self, inventory_id):
        '''
        This method receives an inventory_id
        and searches for a method that has a matching id
        '''
        for inventory in self.inventory_database:
            if inventory["id"] == inventory_id:
                '''
                if an inventory object is found,
                the method returns that object
                '''
                return inventory
            '''
            If nothing was found, the method returns 'None'.
            The user receives a 200 status code and a 'null',
            written in the terminal
            '''
        return None

    def get_inventories_for_item(self, item_id):
        # This method searches for inventory objects with item_id
        found_inventories = []
        for inventory in self.inventory_database:
            '''
            the inventories that contain a matching item_id,
            get put in the result list
            '''
            if inventory["item_id"] == item_id:
                found_inventories.append(inventory)
                # the list gets returned
        return found_inventories

    def get_inventory_totals_for_item(self, item_id):
        '''
         A dictionary is made for the total of items in inventories
        with a matching item id
        '''
        inventory_totals = {
            "total_expected": 0,
            "total_ordered": 0,
            "total_allocated": 0,
            "total_available": 0
        }
        for inventory in self.inventory_database:
            # The system goes through the database
            if inventory["item_id"] == item_id:
                '''
                # if the system finds an inventory object,
                # with a matching item_id
                # it adds the totals of that item to the values 
                # of the result keys
                '''
                for key in [
                    "total_expected",
                    "total_ordered",
                    "total_allocated",
                    "total_available"
                ]:
                    inventory_totals[key] += inventory[key]
                # Then the method returns the totals/result dictionary
        return inventory_totals

    def add_inventory(self, inventory):
        '''
        This method adds/replaces the value of the 'created_at' and
        "updated_at" keys with the current date and time.
        '''
        inventory["created_at"] = self.get_timestamp()
        inventory["updated_at"] = self.get_timestamp()
        # After doing so, it adds the passed inventory object to the database
        self.inventory_database.append(inventory)

    def update_inventory(self, inventory_id, inventory):
        '''
        The method replaces/adds the value of 'updated_at' of the
        passed inventory object with the current date and time 
        '''
        inventory["updated_at"] = self.get_timestamp()
        for inventory in range(len(self.inventory_database)):
            # It loops through the database
            if self.inventory_database[inventory]["id"] == inventory_id:
                '''
                if an inventory object was found with a matching id,
                it replaces all values, with the values of
                the passed inventory object. It replaces the entire object.
                '''
                self.inventory_database[inventory] = inventory
                break

    def remove_inventory(self, inventory_id):
        for inventory in self.inventory_database:
            # The method loops through the database in search of an object
            # that contains the same id as the one passed as a paramter
            if inventory["id"] == inventory_id:
                # Then it deletes the found inventory object
                self.inventory_database.remove(inventory)

    def load(self, is_debug):
        if is_debug:
            self.inventory_database = INVENTORIES
        else:
            f = open(self.inventory_database_path, "r")
            self.inventory_database = json.load(f)
            f.close()

    def save(self):
        f = open(self.inventory_database_path, "w")
        json.dump(self.inventory_database, f)
        f.close()
