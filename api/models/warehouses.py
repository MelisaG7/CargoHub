import json
from models.base import Base

WAREHOUSES = []

class Warehouses(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the Warehouses class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "warehouses.json"
        self.load(is_debug)

    def get_warehouses(self):
        """
        Retrieve all warehouse objects from the JSON file.

        :return: A list of all warehouse objects.
        """
        return self.data

    def get_warehouse(self, warehouse_id):
        """
        Retrieve a warehouse object based on its ID.

        :param warehouse_id: The ID of the warehouse to retrieve.
        :return: A dictionary representing the warehouse if found, otherwise None.
        """
        for warehouse in self.data:
            if warehouse["id"] == warehouse_id:
                return warehouse
        return None

    def add_warehouse(self, warehouse):
        """
        Add a new warehouse object to the JSON data, setting timestamps for creation and update.

        :param warehouse: The dictionary representing the new warehouse to add.
        """
        warehouse["created_at"] = self.get_timestamp()
        warehouse["updated_at"] = self.get_timestamp()
        self.data.append(warehouse)

    def update_warehouse(self, warehouse_id, warehouse):
        """
        Update an existing warehouse based on its ID, replacing it with new data.

        :param warehouse_id: The ID of the warehouse to update.
        :param warehouse: The new data to replace the existing warehouse.
        :return: True if the warehouse was successfully updated; otherwise, False.
        """
        warehouse["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == warehouse_id:
                self.data[i] = warehouse
                return True
        return False

    def remove_warehouse(self, warehouse_id):
        """
        Delete a warehouse based on its ID.

        :param warehouse_id: The ID of the warehouse to remove.
        :return: True if the warehouse was successfully removed; otherwise, False.
        """
        for warehouse in self.data:
            if warehouse["id"] == warehouse_id:
                self.data.remove(warehouse)
                return True
        return False

    def load(self, is_debug):
        """
        Load data from the JSON file or use sample data if in debug mode.

        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        if is_debug:
            self.data = WAREHOUSES
            return
        try:
            with open(self.data_path, "r") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"{self.data_path} not found or could not be loaded.")
            self.data = []

    def save(self):
        """
        Write all current data to the JSON file.
        """
        with open(self.data_path, "w") as file:
            json.dump(self.data, file, indent=4)
