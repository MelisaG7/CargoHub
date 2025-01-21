from models.Models import Inventory
from services.locations import Locations
class InventoriesFoutHandling:

    def __inti__(self):
        self.somthing = "nothing in here idk"
        self.locations = Locations("./data/", False)

    @staticmethod
    def inventories():
        from services.inventories import Inventories
        return Inventories("./data/", False)

    def check_valid_id(self, inventory_id: int):
        # checks on negatieve ids
        if inventory_id < 0:
            return False
        return True

    def check_get_inventory(self, inventory_id: int):
        if not isinstance(inventory_id, int):
            return False
        # Checks on negatieve ids
        return self.check_valid_id(inventory_id)

    def check_get_inventory_for_item(self, item_id):
        # Checks valid item id
        # Ik ga hier en in de methode eronder probs checken of
        # het in database staat.
        # Daarna call ik dit gewoon in de inventories.py
        for inventory in self.inventories().inventory_database:
            if inventory["item_id"] == item_id:
                return True
        return False

    def check_get_inventory_totals_for_item(self, item_id):
        # checks valid item id?
        # Anything else maybe too?
        return self.check_get_inventory_for_item(item_id)

    def check_locations(self, inventory: Inventory):
        for location in inventory.locations:
            location_ids = [loc["location_id"] for loc in self.locations.data]
            if location["location_id"] not in location_ids:
                return False
        return True

    def check_add_inventory(self, inventory: Inventory, inventories):
        if not self.check_locations(inventory):
            return False
        # checks if id not in database
        for inventaris in inventories.inventory_database:
            if inventaris["id"] == inventory.model_dump()["id"]:
                return False
        return True

    def check_put_inventory(self, inventory: Inventory, inventory_id):
        if not self.check_locations(inventory):
            return False
        # checks if id body == id parameter
        if inventory.model_dump()["id"] != inventory_id:
            return False
        return True

    def check_remove_inventory(self, inventory_id):
        # Check on valid Id
        return self.check_valid_id(inventory_id)