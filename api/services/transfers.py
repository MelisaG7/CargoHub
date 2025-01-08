import json
from services.base import Base
from fastapi import APIRouter, HTTPException
from models.Models import Transfer
from fastapi.responses import JSONResponse

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
        self.router = APIRouter()
        self.router.add_api_route(
            "/transfers", self.get_transfers, methods=["GET"])
        self.router.add_api_route(
            "/transfers/{transfer_id}", self.get_transfer, methods=["GET"])
        self.router.add_api_route(
            "/transfers/{transfer_id}/items", self.get_items_in_transfer, methods=["GET"])
        self.router.add_api_route(
            "/transfers", self.add_transfer, methods=["POST"])
        self.router.add_api_route(
            "/transfers/{transfer_id}", self.update_transfer, methods=["PUT"])
        self.router.add_api_route(
            "/transfers/{transfer_id}", self.remove_transfer, methods=["DELETE"])

    def get_transfers(self):
        """Returns a list of all transfer records."""
        return self.data

    def get_transfer(self, transfer_id: int):
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

    def add_transfer(self, transfer: Transfer):
        """Adds a new transfer to the data with an initial status and timestamps.

        Args:
            transfer (dict): The data of the transfer to add.
        """
        transfer_dictionary = transfer.model_dump()
        transfer_dictionary["transfer_status"] = "Scheduled"
        transfer_dictionary["created_at"] = self.get_timestamp()
        transfer_dictionary["updated_at"] = self.get_timestamp()
        self.data.append(transfer_dictionary)
        try:
            return JSONResponse(content="Transfer has been added", status_code=201)
        except Exception as e:
            print(e)

    def update_transfer(self, transfer_id: int, transfer: Transfer):
        """Updates an existing transfer's data by ID.

        Args:
            transfer_id (int): The ID of the transfer to update.
            transfer (dict): The updated transfer data.
        """
        transfer_dictionary = transfer.model_dump()
        transfer_dictionary["updated_at"] = self.get_timestamp()
        for transfers in self.data:
            if transfers["id"] == transfer_id:
                transfers.update(transfer_dictionary)
                return

    def remove_transfer(self, transfer_id: int):
        """Removes a transfer from the data based on its ID.

        Args:
            transfer_id (int): The ID of the transfer to remove.
        """
        for transfer in self.data:
            if transfer["id"] == transfer_id:
                self.data.remove(transfer)

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
