import json

from models.base import Base

TRANSFERS = []

class Transfers(Base):
    def __init__(self, root_path, is_debug=False):
        """Initializes the Transfers class, setting up the path to the data file and loading data.
        
        Args:
            root_path (str): The base path to the data.
            is_debug (bool): If True, loads debug data instead of the JSON file.
        """
        self.data_path = root_path + "transfers.json"
        self.load(is_debug)

    def get_transfers(self):
        """Returns a list of all transfer records."""
        return self.data

    def get_transfer(self, transfer_id):
        """Finds and returns a specific transfer by its ID.
        
        Args:
            transfer_id (int): The ID of the transfer to retrieve.
        
        Returns:
            dict: The transfer data if found, otherwise None.
        """
        for x in self.data:
            if x["id"] == transfer_id:
                return x
        return None

    def get_items_in_transfer(self, transfer_id):
        """Retrieves the items within a specified transfer.
        
        Args:
            transfer_id (int): The ID of the transfer to get items from.
        
        Returns:
            list: A list of items in the transfer, or None if the transfer is not found.
        """
        for x in self.data:
            if x["id"] == transfer_id:
                return x["items"]
        return None

    def add(self, transfer):
        """Adds a new transfer to the data with an initial status and timestamps.
        
        Args:
            transfer (dict): The data of the transfer to add.
        """
        transfer["transfer_status"] = "Scheduled"
        transfer["created_at"] = self.get_timestamp()
        transfer["updated_at"] = self.get_timestamp()
        self.data.append(transfer)

    def update_transfer(self, transfer_id, transfer):
        """Updates an existing transfer's data by ID.
        
        Args:
            transfer_id (int): The ID of the transfer to update.
            transfer (dict): The updated transfer data.
        """
        transfer["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == transfer_id:
                self.data[i] = transfer
                break

    def remove_transfer(self, transfer_id):
        """Removes a transfer from the data based on its ID.
        
        Args:
            transfer_id (int): The ID of the transfer to remove.
        """
        for x in self.data:
            if x["id"] == transfer_id:
                self.data.remove(x)

    def load(self, is_debug):
        """Loads transfer data from a JSON file or debug data if specified.
        
        Args:
            is_debug (bool): If True, loads debug data instead of reading from the JSON file.
        """
        if is_debug:
            self.data = TRANSFERS
        else:
            f = open(self.data_path, "r")
            self.data = json.load(f)
            f.close()

    def save(self):
        """Saves the current transfer data to the JSON file."""
        f = open(self.data_path, "w")
        json.dump(self.data, f)
        f.close()
