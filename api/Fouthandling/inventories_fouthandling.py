class InventoriesFoutHandling:

    def __init__(self):
        self.RequiredFields = [
            "id", "item_id", "description",
            "item_reference", "locations", "total_on_hand",
            "total_expected", "total_ordered", "total_allocated",
            "total_available"
        ]

    def inventories():
        from models.inventories import Inventories
        return Inventories("", True)

    def check_valid_id(self, inventory_id):
        # checks on negatieve ids
        if inventory_id < 0:
            return False
        return True

    def check_valid_body(self, inventory):
        # checks on valid json body
        # checks if body has all required fields
        for field in self.RequiredFields:
            if field not in inventory:
                return False
        return True

    def check_get_inventory(self, inventory_id):
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

    def check_add_inventory(self, inventory):
        # checks valid body
        if self.check_valid_body(inventory):
            # checks if id not in database
            for inventaris in self.inventories().inventory_database:
                if inventaris["id"] == inventory["id"]:
                    return False
        return True

    def check_put_inventory(self, inventory, inventory_id):
        # checks valid body
        if self.check_valid_body(self, inventory):
            # checks if id body == id parameter
            if inventory["id"] != inventory_id:
                return False
        return True

    def check_remove_inventory(self, inventory_id):
        # Check on valid Id
        return self.check_valid_id(inventory_id)
