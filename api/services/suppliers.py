import json

from services.base import Base

SUPPLIERS = []

class Suppliers(Base):
    def __init__(self, root_path, is_debug=False):
        """Initializes the Suppliers class with the path to the JSON file and loads the data.
        
        Args:
            root_path (str): Base path to the data.
            is_debug (bool): Indicates if debug data should be loaded.
        """
        self.data_path = root_path + "suppliers.json"
        self.load(is_debug)

    def get_suppliers(self):
        """Returns a list of all suppliers stored in the data."""
        return self.data

    def get_supplier(self, supplier_id):
        """Finds a specific supplier by ID and returns it as a dictionary.
        
        Args:
            supplier_id (int): ID of the supplier to retrieve.
        
        Returns:
            dict: The supplier data if found, otherwise None.
        """
        for supplier in self.data:
            if supplier["id"] == supplier_id:
                return supplier
        return None

    def add(self, supplier):
        """Adds a new supplier to the data with created and updated timestamps.
        
        Args:
            supplier (dict): The data of the supplier to add.
        """
        supplier["created_at"] = self.get_timestamp()
        supplier["updated_at"] = self.get_timestamp()
        self.data.append(supplier)

    def update_supplier(self, supplier_id, supplier):
        """Updates an existing supplier based on the supplier ID.
        
        Args:
            supplier_id (int): ID of the supplier to update.
            supplier (dict): The updated supplier data.
        """
        supplier["updated_at"] = self.get_timestamp()
        for index in range(len(self.data)):
            if self.data[index]["id"] == supplier_id:
                self.data[index] = supplier
                break

    def remove_supplier(self, supplier_id):
        """Removes a supplier from the data based on the supplier ID.
        
        Args:
            supplier_id (int): ID of the supplier to remove.
        """
        for supplier in self.data:
            if supplier["id"] == supplier_id:
                self.data.remove(supplier)

    def load(self, is_debug):
        """Loads supplier data from JSON or debug data.
        
        Args:
            is_debug (bool): If True, loads debug data instead of the JSON file.
        """
        if is_debug:
            self.data = SUPPLIERS
        else:
            f = open(self.data_path, "r")
            self.data = json.load(f)
            f.close()

    def save(self):
        """Saves the current data to the JSON file."""
        f = open(self.data_path, "w")
        json.dump(self.data, f)
        f.close()
