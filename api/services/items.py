import json
import re
from services.base import Base

from fastapi import APIRouter, HTTPException
from models.Models import Item
from fastapi.responses import JSONResponse



class Items(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the Items class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "items.json"
        self.is_debug = is_debug
        self.data = []

        self.required_fields = [
            "uid", 
            "code", 
            "description", 
            "short_description", 
            "upc_code", 
            "model_number", 
            "commodity_code", 
            "item_line", 
            "item_group", 
            "item_type", 
            "unit_purchase_quantity", 
            "unit_order_quantity", 
            "pack_order_quantity", 
            "supplier_id", 
            "supplier_code", 
            "supplier_part_number"
        ]
        self.load(is_debug)

        self.router = APIRouter() 

        self.router.add_api_route("/items", self.get_items, methods=["GET"])
        self.router.add_api_route("/items/{item_uid}", self.get_item, methods=["GET"])

        self.router.add_api_route("/items/item_line/{item_line_id}", self.get_items_for_item_line, methods=["GET"])
        self.router.add_api_route("/items/item_group/{item_group_id}", self.get_items_for_item_group, methods=["GET"])
        self.router.add_api_route("/items/item_type/{item_type_id}", self.get_items_for_item_type, methods=["GET"])
        self.router.add_api_route("/items/supplier/{supplier_id}", self.get_items_for_supplier, methods=["GET"])

        self.router.add_api_route("/items", self.add_item, methods=["POST"])
        self.router.add_api_route("/items/{item_uid}", self.update_item, methods=["PUT"])
        self.router.add_api_route("/items/{item_uid}", self.remove_item, methods=["DELETE"])

    def is_valid_uid(self, uid: str):
            """
            Check if a given uid is valid. A valid uid starts with 'P', followed by any number of digits, and ends with a digit.

            :param uid: The uid string to validate.
            :return: True if the uid is valid, otherwise False.
            """
            pattern = r"^P\d+$"  # 'P' followed by one or more digits, and must end with a digit.
            return bool(re.match(pattern, uid))
        
    def validate_item(self, item: dict):
        for field in self.required_fields:
            if field not in item:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        return True 

    def get_items(self):
        """
        Retrieve all items from json.

        :return: A list of all items.
        """
        return self.data

    def get_item(self, item_uid:str):
        """
        Retrieve an item based on uid.

        :param item_uid: The unique identifier for the item.
        :return: The item dictionary if found, or exception if not found.
        """
    
        if not self.is_valid_uid(item_uid):
            raise HTTPException(status_code=400,
                                detail=f"Invalid uid: {item_uid}")

        for item in self.data:
            if item["uid"] == item_uid:
                return item
        # return   
        raise HTTPException(status_code=404,
                                detail=f"Itemline with id {item_uid} was not found")
   

# for this method to be implemented the main needs to be refactored
    def get_items_for_field(self, field:str, id:int):
        """
        Retrieve all items based on the given field id.

        :param field: The field name to filter by.
        :param value: The value of the field to match.
        :return: A list of items matching the specified field and value.
        """
        result = []
        if id < 0:
            raise HTTPException(status_code=400, detail=f"Invalid id: {id}")
        for item in self.data:
            if item[field] == id:
                result.append(item)
        return result

    def get_items_for_item_line(self, item_line_id:int):
        """
        Retrieve all items with the given item line ID.

        :param item_line_id: The item line ID to filter by.
        :return: A list of items matching the item line ID.
        """
        return self.get_items_for_field("item_line", item_line_id)

    def get_items_for_item_group(self, item_group_id:int):
        """
        Retrieve all items with the given item group ID.

        :param item_group_id: The item group ID to filter by.
        :return: A list of items matching the item group ID.
        """
        return self.get_items_for_field("item_group", item_group_id)

    def get_items_for_item_type(self, item_type_id:int):
        """
        Retrieve all items with the given item type ID.

        :param item_type_id: The item type ID to filter by.
        :return: A list of items matching the item type ID.
        """
        return self.get_items_for_field("item_type", item_type_id)

    def get_items_for_supplier(self, supplier_id:int):
        """
        Retrieve all items with the given supplier ID.

        :param supplier_id: The supplier ID to filter by.
        :return: A list of items matching the supplier ID.
        """
        return self.get_items_for_field("supplier_id", supplier_id)

    def add_item(self, item:Item):
        """
        Add a new item to the data with timestamps for creation and update.

        :param item: The item data to add.
        """
        item_dict = item.model_dump()

        self.validate_item(item_dict) # checks whether item_type has the correct body
        if not self.is_debug:
            self.load(self.is_debug)

        # Loops through the existing to data if there already is an item type with the same id
        for item in self.data:
            if item["uid"] == item_dict["uid"]:
                raise HTTPException(status_code=400, detail="There already is a item with the same uid")

        '''
        # The server adds/replaces the 'created_at' and 'updated_at',
        # with the current date and time.
        '''
        item_data = item_dict
        item_data["created_at"] = self.get_timestamp()
        item_data["updated_at"] = self.get_timestamp()
        self.data.append(item_data)

        if not self.is_debug: # checks whether the unittests are ran
            self.save()
        # changes the status code to 201 Created instead of 200 OK with a message
        return JSONResponse(content="Item was succesfully added to the database", status_code=201) 

    def update_item(self, item_uid:str, new_item:Item):
        """
        Update an existing item with new data based on its ID.

        :param item_id: The unique identifier of the item to update.
        :param new_item: The new item data to update.
        :return: True if item was updated, False if item was not found.
        """
        self.validate_item(new_item.model_dump())
        
        
        if self.get_item(item_uid) is None or not self.is_valid_uid(item_uid):
            raise HTTPException(status_code=400,
                                detail="Invalid uid or can't find the item to be updated")
        new_item_dict = new_item.model_dump()

        for item in self.data:
            if item["uid"] == item_uid:
                new_item_dict["updated_at"] = self.get_timestamp()
                item.update(new_item_dict)
                if not self.is_debug:
                    self.save()
                return {"message": "Item successfully updated."}
        return {"message: Item not updated"}

    def remove_item(self, item_uid:str):
        """
        Remove an item from the data based on its ID.

        :param item_id: The unique identifier of the item to remove.
        :return: True if item was removed, False if item was not found.
        """
        if not self.is_debug:
            self.load(self.is_debug)
        if self.get_item(item_uid) is None or not self.is_valid_uid(item_uid):
            raise HTTPException(status_code=400,                              
                                detail=f"Invalid uid: {item_uid} or item doesnt exist")
        
        for item in self.data:
            if item["uid"] == item_uid:
                self.data.remove(item)
                if not self.is_debug:
                    self.save()
                return {"message":
                        "itemline successfully removed from the database."}
        return {"message":"Item not found"}
    
    def load(self, is_debug):
        """
        Load data from the JSON file.

        :param is_debug: If False, loads sample data; otherwise, nothing.   
        """
        if not is_debug:
            try:
                with open(self.data_path, "r") as file:
                    self.data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                print(self.data_path + " not found or couldn't be loaded")
                self.data = []

    def save(self):
        """
        Save the current data to the JSON file.
        """
        try:
            with open(self.data_path, "w") as file:
                json.dump(self.data, file, indent=4)
        except(FileNotFoundError, json.JSONDecodeError):
            raise HTTPException(f"{self.data_path} not found or could not be loaded.") 