import json

from models.base import Base

ITEM_TYPES = []


class ItemTypes(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the ItemTypes class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "item_types.json"
        self.load(is_debug)

    def get_item_types(self):
        """
        Retrieve all item type objects from the JSON file.

        :return: A list of all item type objects.
        """
        return self.data

    def get_item_type(self, item_type_id):
        """
        Retrieve an item type object based on its ID.

        :param item_type_id: The ID of the item type to retrieve.
        :return: A dictionary representing the item type if found, otherwise None.
        """
        for item_type in self.data:
            if item_type["id"] == item_type_id:
                return item_type
        return None

    def add(self, item_type):
        """
        Add a new item type object to the JSON data, setting timestamps for creation and update.

        :param item_type: The dictionary representing the new item type to add.
        """
        item_type["created_at"] = self.get_timestamp()
        item_type["updated_at"] = self.get_timestamp()
        self.data.append(item_type)

    def update_item_type(self, item_type_id, new_item_type):
        """
        Update an existing item type based on its ID, replacing it with new data.

        :param item_type_id: The ID of the item type to update.
        :param new_item_type: The new data to replace the existing item type.
        :return: True if the item type was successfully updated; otherwise, False.
        """
        new_item_type["updated_at"] = self.get_timestamp()
        for itemtype in range(len(self.data)):
            if self.data[itemtype]["id"] == item_type_id:
                self.data[itemtype] = new_item_type
                return True
        return False

    def remove_item_type(self, item_type_id):
        """
        Delete an item type based on its ID.

        :param item_type_id: The ID of the item type to remove.
        :return: True if the item type was successfully removed; otherwise, False.
        """
        for item_type in self.data:
            if item_type["id"] == item_type_id:
                self.data.remove(item_type)
                return True
        return False

    def load(self, is_debug):
        """
        Load data from the JSON file or use sample data if in debug mode.

        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        if is_debug:
            self.data = ITEM_TYPES
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