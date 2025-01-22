from models.Models import Inventory


class InventoriesFoutHandling:

    def __inti__(self):
        self.somthing = "nothing in here idk"

    @staticmethod
    def inventories():
        from services.inventories import Inventories
        return Inventories("./data/", False)

    @staticmethod
    def locations():
        from services.locations import Locations
        return Locations("./data/", False)

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
        try:
            locations = [loc["id"] for loc in self.locations().data]
            for location in inventory.locations:
                if location not in locations:
                    return False
            return True
        except Exception as e:
            print(e)
            return False

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