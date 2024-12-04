import json

from services.base import Base
# from providers import data_provider

SHIPMENTS = []

# CHANGES:
# Functie DataProvider() returned data_provider
# Deze wordt opgeroepen waar nodig is ipv data_provider


class Shipments(Base):
    def __init__(self, root_path, is_debug=False):
        """Initializes the Shipments class with the path to the JSON file and loads the data.

        Args:
            root_path (str): Base path to the data.
            is_debug (bool): Indicates if debug data should be loaded.
        """
        self.data_path = root_path + "shipments.json"
        self.load(is_debug)
    
    def DataProvider():
        from providers import data_provider
        return data_provider

    def get_shipments(self):
        """Returns a list of all shipments stored in the data."""
        return self.data

    def get_shipment(self, shipment_id):
        """Finds a specific shipment by ID and returns it as a dictionary.
        
        Args:
            shipment_id (int): ID of the shipment to retrieve.
        
        Returns:
            dict: The shipment data if found, otherwise None.
        """
        for shipment in self.data:
            if shipment["id"] == shipment_id:
                return shipment
        return None

    def get_items_in_shipment(self, shipment_id):
        """Fetches all items within a specific shipment.
        
        Args:
            shipment_id (int): ID of the shipment whose items to retrieve.
        
        Returns:
            list: A list of items in the shipment, or None if the shipment does not exist.
        """
        for shipment in self.data:
            if shipment["id"] == shipment_id:
                return shipment["items"]
        return None

    def add(self, shipment):
        """Adds a new shipment to the data with created and updated timestamps.
        
        Args:
            shipment (dict): The data of the shipment to add.
        """
        shipment["created_at"] = self.get_timestamp()
        shipment["updated_at"] = self.get_timestamp()
        self.data.append(shipment)

    def update_shipment(self, shipment_id, shipment):
        """Updates an existing shipment based on the shipment ID.
        
        Args:
            shipment_id (int): ID of the shipment to update.
            shipment (dict): The updated shipment data.
        """
        shipment["updated_at"] = self.get_timestamp()
        for index in range(len(self.data)):
            if self.data[index]["id"] == shipment_id:
                self.data[index] = shipment
                break

    def update_items_in_shipment(self, shipment_id, items):
        """Updates the items within a shipment and manages inventory.

        Args:
            shipment_id (int): ID of the shipment to update.
            updated_items (list): The updated list of items within the shipment.
        """
        # Retrieve the current shipment and its items
        shipment = self.get_shipment(shipment_id)
        current_items = shipment["items"]

        # Remove items that are no longer in the shipment
        for current_item in current_items:
            item_still_exists = False
            for updated_item in items:
                if current_item["item_id"] == updated_item["item_id"]:
                    item_still_exists = True
                    break
            if not item_still_exists:
                inventories = self.DataProvider().fetch_inventory_pool().get_inventories_for_item(current_item["item_id"])
                highest_ordered = -1
                selected_inventory = None

                for inventory in inventories:
                    if inventory["total_ordered"] > highest_ordered:
                        highest_ordered = inventory["total_ordered"]
                        selected_inventory = inventory

                if selected_inventory:
                    selected_inventory["total_ordered"] -= current_item["amount"]
                    selected_inventory["total_expected"] = (
                        selected_inventory["total_on_hand"] + selected_inventory["total_ordered"]
                    )
                    self.DataProvider().fetch_inventory_pool().update_inventory(selected_inventory["id"], selected_inventory)

        # Add or update items in the shipment
        for updated_item in items:
            matching_item = None
            for current_item in current_items:
                if current_item["item_id"] == updated_item["item_id"]:
                    matching_item = current_item
                    break

            if matching_item:
                # Update inventory for the existing item
                inventories = self.DataProvider().fetch_inventory_pool().get_inventories_for_item(matching_item["item_id"])
                highest_ordered = -1
                selected_inventory = None

                for inventory in inventories:
                    if inventory["total_ordered"] > highest_ordered:
                        highest_ordered = inventory["total_ordered"]
                        selected_inventory = inventory

                if selected_inventory:
                    selected_inventory["total_ordered"] += updated_item["amount"] - matching_item["amount"]
                    selected_inventory["total_expected"] = (
                        selected_inventory["total_on_hand"] + selected_inventory["total_ordered"]
                    )
                    self.DataProvider().fetch_inventory_pool().update_inventory(selected_inventory["id"], selected_inventory)

        # Replace the shipment's items with the updated items
        shipment["items"] = items
        self.update_shipment(shipment_id, shipment)

    def remove_shipment(self, shipment_id):
        """Removes a shipment from the data based on the shipment ID.
        
        Args:
            shipment_id (int): ID of the shipment to remove.
        """
        for shipment in self.data:
            if shipment["id"] == shipment_id:
                self.data.remove(shipment)

    def load(self, is_debug):
        """Loads shipment data from JSON or debug data.
        
        Args:
            is_debug (bool): If True, loads debug data instead of the JSON file.
        """
        if is_debug:
            self.data = SHIPMENTS
        else:
            f = open(self.data_path, "r")
            self.data = json.load(f)
            f.close()

    def save(self):
        """Saves the current data to the JSON file."""
        f = open(self.data_path, "w")
        json.dump(self.data, f)
        f.close()
