import json

from services.base import Base
from processors import notification_processor
from providers import data_provider


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
        for transfer in self.data:
            if transfer["id"] == transfer_id:
                return transfer
        return None

    def get_items_in_transfer(self, transfer_id):
        """Retrieves the items within a specified transfer.
        
        Args:
            transfer_id (int): The ID of the transfer to get items from.
        
        Returns:
            list: A list of items in the transfer, or None if the transfer is not found.
        """
        for transfer in self.data:
            if transfer["id"] == transfer_id:
                return transfer["items"]
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
        for index in range(len(self.data)):
            if self.data[index]["id"] == transfer_id:
                self.data[index] = transfer
                break

    def remove_transfer(self, transfer_id):
        """Removes a transfer from the data based on its ID.
        
        Args:
            transfer_id (int): The ID of the transfer to remove.
        """
        for transfer in self.data:
            if transfer["id"] == transfer_id:
                self.data.remove(transfer)
    '''
    This method under was previously in the put_requests file,
    but it made the code too messy.
    Since this only happnes in transfers and with transfer objects,
    I decided to move this to transfers.py
    '''
    def process_commit(self, transfer):
        # Transfer object ^
        for item in transfer["items"]:
            # loops through the collection in the key
            # 'items' of the transfer object
            inventories = data_provider.POOL_DICT[
                "inventories"].get_inventories_for_item(item["item_id"])
            # For every item it accesses its inventories
            # with help of its unique item id
            for inventory in inventories:
                # for every inventory of that item:
                if inventory["location_id"] == transfer["transfer_from"]:
                    inventory["total_on_hand"] -= item["amount"]
                elif inventory["location_id"] == transfer["transfer_to"]:
                    inventory["total_on_hand"] += item["amount"]
                inventory["total_expected"] = inventory["total_on_hand"] + inventory["total_ordered"]
                inventory["total_available"] = inventory["total_on_hand"] - inventory["total_allocated"]
                data_provider.POOL_DICT["inventories"].update(inventory["id"], inventory)
                # After doing some shit and
                # updating every inventory it gives a message:
        transfer["transfer_status"] = "Processed"
        # the message is processed 
        # given by the transfer_status key in transfer object
        notification_processor.push(
            f"Processed batch transfer with id:{transfer['id']}")
        # It pushes that message to the terminal I guess?

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
