import json

from models.base import Base

ITEMS = []


class Items(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the Items class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "items.json"
        self.load(is_debug)

    def get_items(self):
        """
        Retrieve all items from json.

        :return: A list of all items.
        """
        return self.data

    def get_item(self, item_id):
        """
        Retrieve an item based on uid.

        :param item_id: The unique identifier for the item.
        :return: The item dictionary if found, or None if not found.
        """
        for item in self.data:
            if item["uid"] == item_id:
                return item
        return None

# for this method to be implemented the main needs to be refactored
    def get_items_for_field(self, field, id):
        """
        Retrieve all items based on the given field id.

        :param field: The field name to filter by.
        :param value: The value of the field to match.
        :return: A list of items matching the specified field and value.
        """
        result = []
        for item in self.data:
            if item[field] == id:
                result.append(item)
        return result

    def get_items_for_item_line(self, item_line_id):
        """
        Retrieve all items with the given item line ID.

        :param item_line_id: The item line ID to filter by.
        :return: A list of items matching the item line ID.
        """
        return self.get_items_for_field("item_line", item_line_id)

    def get_items_for_item_group(self, item_group_id):
        """
        Retrieve all items with the given item group ID.

        :param item_group_id: The item group ID to filter by.
        :return: A list of items matching the item group ID.
        """
        return self.get_items_for_field("item_group", item_group_id)

    def get_items_for_item_type(self, item_type_id):
        """
        Retrieve all items with the given item type ID.

        :param item_type_id: The item type ID to filter by.
        :return: A list of items matching the item type ID.
        """
        return self.get_items_for_field("item_type", item_type_id)

    def get_items_for_supplier(self, supplier_id):
        """
        Retrieve all items with the given supplier ID.

        :param supplier_id: The supplier ID to filter by.
        :return: A list of items matching the supplier ID.
        """
        return self.get_items_for_field("supplier_id", supplier_id)

    def add_item(self, item):
        """
        Add a new item to the data with timestamps for creation and update.

        :param item: The item data to add.
        """
        item["created_at"] = self.get_timestamp()
        item["updated_at"] = self.get_timestamp()
        self.data.append(item)
        self.save()

    def update_item(self, item_id, new_item):
        """
        Update an existing item with new data based on its ID.

        :param item_id: The unique identifier of the item to update.
        :param new_item: The new item data to update.
        :return: True if item was updated, False if item was not found.
        """
        for item in range(len(self.data)):
            if self.data[item]["uid"] == item_id:
                new_item["updated_at"] = self.get_timestamp()
                self.data[item] = new_item
                self.save()
                return True
        return False

    def remove_item(self, item_id):
        """
        Remove an item from the data based on its ID.

        :param item_id: The unique identifier of the item to remove.
        :return: True if item was removed, False if item was not found.
        """
        for item in self.data:
            if item["uid"] == item_id:
                self.data.remove(item)
                self.save()
                return True
        return False

    def load(self, is_debug):
        """
        Load data from the JSON file, or use sample data if in debug mode.

        :param is_debug: If True, loads sample data; otherwise, loads data from file.   
        """
        if is_debug:
           self.data = ITEMS
           return
        try:
            with open(self.data_path, "r") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(self.data_path + " not found")
            self.data = []

    def save(self) -> None:
        """
        Save the current data to the JSON file.
        """
        with open(self.data_path, "w") as file:
            json.dump(self.data, file, indent=4)