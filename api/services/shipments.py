import json
from services.base import Base
from fastapi import APIRouter, HTTPException
from models.Models import Shipment
from fastapi.responses import JSONResponse
from services.inventories import Inventories


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
        self.is_debug = is_debug
        self.load(is_debug)
        self.required_fields = [
            "id",
            "order_id",
            "source_id",
            "order_date",
            "request_date",
            "shipment_date",
            "shipment_type",
            "shipment_status",
            "notes",
            "carrier_code",
            "carrier_description",
            "service_code",
            "payment_type",
            "transfer_mode",
            "total_package_count",
            "total_package_weight",
            "items"
        ]


        self.router = APIRouter()

        self.router.add_api_route(
            "/shipments/", self.get_shipments, methods=["GET"])
        self.router.add_api_route(
            "/shipments/{shipment_id}", self.get_shipment, methods=["GET"])
        self.router.add_api_route(
            "/shipments/{shipment_id}/items", self.get_items_in_shipment, methods=["GET"])
        self.router.add_api_route(
            "/shipments/", self.add_shipment, methods=["POST"])
        self.router.add_api_route(
            "/shipments/{shipment_id}", self.update_shipment, methods=["PUT"])
        self.router.add_api_route(
            "/shipments/{shipment_id}/items", self.update_items_in_shipment, methods=["PUT"])
        self.router.add_api_route(
            "/shipments/{shipment_id}", self.remove_shipment, methods=["DELETE"])

    def validate_shipment(self, shipment: dict):
        for field in self.required_fields:
            if field not in shipment:
                raise HTTPException(
                    status_code=400, detail=f"Missing required field: {field}")
        return True
    
    def DataProvider():
        from providers import data_provider
        return data_provider
    
    def get_shipments(self):
        """Returns a list of all shipments stored in the data."""
        return self.data

    def get_shipment(self, shipment_id: int):
        """Finds a specific shipment by ID and returns it as a dictionary.

        Args:
            shipment_id (int): ID of the shipment to retrieve.

        Returns:
            dict: The shipment data if found, otherwise None.
        """
  
        if shipment_id <= 0:
            raise HTTPException(status_code=400,
                                detail=f"Invalid id: {shipment_id}")

        for shipment in self.data:
            if shipment["id"] == shipment_id:
                return shipment

        raise HTTPException(status_code=204,
                            detail=f"Shipment with id {shipment_id} was not found")
  

    def get_items_in_shipment(self, shipment_id: int):
        """Fetches all items within a specific shipment.

        Args:
            shipment_id (int): ID of the shipment whose items to retrieve.

        Returns:
            list: A list of items in the shipment, or None if the shipment does not exist.
        """
        items = self.get_shipment(shipment_id)
        if len(items["items"]) is None:
            raise HTTPException(status_code=204,
                            detail=f"There are no items with id {shipment_id} was not found")
        return items["items"]
        

    def add_shipment(self, shipment: Shipment):
        """Adds a new shipment to the data with created and updated timestamps.

        Args:
            shipment (dict): The data of the shipment to add.
        """
        shipment_dictionary = shipment.model_dump()
        # self.validate_shipment(shipment_dictionary)

        # loads data to get up to date json file
        if not self.is_debug:
            self.load(self.is_debug)

        # checks whether there already is a shipment with the same id
        for shipment in self.data:
            if shipment["id"] == shipment_dictionary["id"]:
                raise HTTPException(
                    status_code=400, detail="There already is shipment with the same id")
                    
        shipment_dictionary["created_at"] = self.get_timestamp()
        shipment_dictionary["updated_at"] = self.get_timestamp()
        self.data.append(shipment_dictionary)
        if not self.is_debug:  # checks whether the unittests are ran
            self.save()
        return JSONResponse(content="Shipment was succesfully added to the database", status_code=201)


    def update_shipment(self, shipment_id: int, new_shipment: Shipment):
        """Updates an existing shipment based on the shipment ID.

        Args:
            shipment_id (int): ID of the shipment to update.
            shipment (dict): The updated shipment data.
        """
        # get newest data from json
        if not self.is_debug:
            self.load(self.is_debug)
        if self.get_shipment(shipment_id) is None or shipment_id < 0:
            raise HTTPException(status_code=204,
                                detail="Invalid shipment id or can't find the shipment to be updated")
        
        shipment_dictionary = new_shipment.model_dump()
        shipment_dictionary["updated_at"] = self.get_timestamp()

        for old_shipment in self.data:
            if old_shipment["id"] == shipment_id:
                old_shipment.update(shipment_dictionary)
                if not self.is_debug:
                    self.save()
                return {"message": "Shipment successfully updated."}


    def update_items_in_shipment(self, shipment_id, items):
        """Updates the items within a shipment and manages inventory.

        Args:
            shipment_id (int): ID of the shipment to update.
            updated_items (list): The updated list of items within the shipment.
        """
        inventoriesObject = Inventories("./data/", False)
        # Retrieve the current shipment and its items
        shipment = self.get_shipment(shipment_id)
        if shipment is None:
                raise HTTPException(
                    status_code=204, detail=f"Shipment with id {shipment_id} not found")
        if len(items) < 1:
            raise HTTPException(
                    status_code=204, detail=f"List with updated items is empty")

        current_items = shipment["items"]

        # Remove items that are no longer in the shipment
        for current_item in current_items:
            item_still_exists = False
            for updated_item in items:
                if current_item["item_id"] == updated_item["item_id"]:
                    item_still_exists = True
                    break

            if not item_still_exists:
                inventories = inventoriesObject.get_inventories_for_item(current_item["item_id"])
                highest_ordered = -1
                selected_inventory = None

                for inventory in inventories:
                    if inventory["total_ordered"] > highest_ordered:
                        highest_ordered = inventory["total_ordered"]
                        selected_inventory = inventory

                if selected_inventory:
                    selected_inventory["total_ordered"] -= current_item["amount"]
                    selected_inventory["total_expected"] = (
                        selected_inventory["total_on_hand"] +
                        selected_inventory["total_ordered"]
                    )
                    inventoriesObject.update_inventory(
                        selected_inventory["id"], selected_inventory)

        # Add or update items in the shipment
        for updated_item in items:
            matching_item = None
            for current_item in current_items:
                if current_item["item_id"] == updated_item["item_id"]:
                    matching_item = current_item
                    break

            if matching_item:
                # Update inventory for the existing item
                inventories = inventoriesObject.get_inventories_for_item(matching_item["item_id"])
                highest_ordered = -1
                selected_inventory = None

                for inventory in inventories:
                    if inventory["total_ordered"] > highest_ordered:
                        highest_ordered = inventory["total_ordered"]
                        selected_inventory = inventory

                if selected_inventory:
                    selected_inventory["total_ordered"] += updated_item["amount"] - \
                        matching_item["amount"]
                    selected_inventory["total_expected"] = (
                        selected_inventory["total_on_hand"] +
                        selected_inventory["total_ordered"]
                    ) 
                    inventoriesObject.update_inventory(
                        selected_inventory["id"], selected_inventory)

        # Replace the shipment's items with the updated items
        shipment["items"] = items
        self.update_shipment(shipment_id, shipment)
        return {"message":
            "Items in shipment successfully updated in the database."}


    def remove_shipment(self, shipment_id):
        """Removes a shipment from the data based on the shipment ID.

        Args:
            shipment_id (int): ID of the shipment to remove.
        """
        try:
            # refreshes data
            if not self.is_debug:
                self.load(self.is_debug)
            shipment_id = int(shipment_id)

            if shipment_id < 0:
                raise HTTPException(status_code=400,
                                    detail=f"Invalid shipment id: {shipment_id} ")
            
            for shipment in self.data:
                if shipment["id"] == shipment_id:
                    self.data.remove(shipment)
                    if not self.is_debug:
                        self.save()
                    return {"message":
                        "shipment successfully removed from the database."}
            raise HTTPException(status_code=400,
                                    detail=f"Invalid shipment id: {shipment_id} or shipment doesnt exist")
        except Exception as e:
            print(e)

    def load(self, is_debug):
        """Loads shipment data from JSON or debug data.

        Args:
            is_debug (bool): If True, loads debug data instead of the JSON file.
        """
        if not is_debug:
            try:
                # loads data from json
                with open(self.data_path, "r") as file:
                    self.data = json.load(file)
            # raised exception if file not found or file couldn't be read
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"{self.data_path} not found or could not be loaded.")
                self.data = []

    def save(self):
        """Saves the current data to the JSON file."""
        try:
            with open(self.data_path, "w") as file:
                json.dump(self.data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            raise HTTPException(
                f"{self.data_path} not found or could not be loaded.")
