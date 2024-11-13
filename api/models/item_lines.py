import json
from models.base import Base

ITEM_LINES = []

class ItemLines(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the ItemLines class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "item_lines.json"
        self.load(is_debug)

    def get_item_lines(self):
        """
        Retrieve all item lines from the JSON data.

        :return: A list of all item line objects.
        """
        return self.data

    def get_item_line(self, item_line_id):
        """
        Retrieve a specific item line based on its ID.

        :param item_line_id: The unique identifier for the item line.
        :return: The item line dictionary if found, otherwise None.
        """
        for item_line in self.data:
            if item_line["id"] == item_line_id:
                return item_line
        return None

    def add_item_line(self, item_line):
        """
        Add a new item line to the JSON data with timestamps for creation and update.

        :param item_line: A dictionary representing the new item line to add.
        """
        item_line["created_at"] = self.get_timestamp()
        item_line["updated_at"] = self.get_timestamp()
        self.data.append(item_line)
        self.save()

    def update_item_line(self, item_line_id, new_item_line):
        """
        Update an existing item line with new data, based on its ID.

        :param item_line_id: The unique identifier for the item line to update.
        :param new_item_line: A dictionary containing updated data for the item line.
        :return: True if the item line was successfully updated; otherwise, False.
        """
        new_item_line["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == item_line_id:
                self.data[i] = new_item_line
                self.save()
                return True
        return False

    def remove_item_line(self, item_line_id):
        """
        Remove an item line from the JSON data based on its ID.

        :param item_line_id: The unique identifier for the item line to remove.
        :return: True if the item line was successfully removed; otherwise, False.
        """
        for item_line in self.data:
            if item_line["id"] == item_line_id:
                self.data.remove(item_line)
                self.save()
                return True
        return False

    def load(self, is_debug):
        """
        Load item line data from the JSON file, or use sample data if in debug mode.

        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        if is_debug:
            self.data = ITEM_LINES
            return
        try:
            with open(self.data_path, "r") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"{self.data_path} not found or could not be loaded.")
            self.data = []

    def save(self):
        """
        Write all current item line data to the JSON file.
        """
        with open(self.data_path, "w") as file:
            json.dump(self.data, file, indent=4)
