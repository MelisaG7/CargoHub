import json
from services.base import Base

from fastapi import APIRouter, HTTPException
from models.Models import ItemType
from fastapi.responses import JSONResponse




class ItemTypes(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the ItemTypes class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "item_types.json"
        self.is_debug = is_debug
        self.data = []
        self.required_fields = [
            "id", "name", "description"
        ]
        self.load(is_debug)

        self.router = APIRouter()

        self.router.add_api_route("/item_types", self.get_item_types, methods=["GET"])
        self.router.add_api_route("/item_types/{item_type_id}", self.get_item_type, methods=["GET"])
        self.router.add_api_route("/item_types", self.add_item_type, methods=["POST"])
        self.router.add_api_route("/item_types/{item_type_id}", self.update_item_type, methods=["PUT"])
        self.router.add_api_route("/item_types/{item_type_id}", self.remove_item_type, methods=["DELETE"])

    def check_valid_id(self, item_type_id: int):
        """
        Check if the provided ID is valid (non-negative).

        :param item_type_id: The unique identifier to validate.
        :return: True if the ID is valid, False otherwise.
        """
        return item_type_id >= 0
    
    def validate_item_type(self, item_type: dict):
        for field in self.required_fields:
            if field not in item_type:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        return True 
    
    def get_item_types(self):
        """
        Retrieve all item type objects from the JSON file.

        :return: A list of all item type objects.
        """
        return self.data

    def get_item_type(self, item_type_id:int):
        """
        Retrieve an item type object based on its ID.

        :param item_type_id: The ID of the item type to retrieve.
        :return: A dictionary representing the item type if found, otherwise None.
        """
        try:
            if not self.check_valid_id(item_type_id):
                raise HTTPException(status_code=400,
                                    detail=f"Invalid id: {item_type_id}")

            for item_type in self.data:
                if item_type["id"] == item_type_id:
                    return item_type
                
            raise HTTPException(status_code=404,
                                    detail=f"Itemline with id {item_type_id} was not found")
        except Exception as e:
            print(e)

    def add_item_type(self, item_type:ItemType):
        """
        Add a new item type object to the JSON data, setting timestamps for creation and update.

        :param item_type: The dictionary representing the new item type to add.
        """
        item_type_dict = item_type.model_dump()

        self.validate_item_type(item_type_dict) # checks whether item_type has the correct body
        if not self.is_debug:
            self.load(self.is_debug)

        # Loops through the existing to data if there already is an item type with the same id
        for line in self.data:
            if line["id"] == item_type_dict["id"]:
                raise HTTPException(status_code=400, detail="There already is a itemtype with the same id")

        '''
        # The server adds/replaces the 'created_at' and 'updated_at',
        # with the current date and time.
        '''
        itemtype_data = item_type_dict
        itemtype_data["created_at"] = self.get_timestamp()
        itemtype_data["updated_at"] = self.get_timestamp()
        self.data.append(itemtype_data)

        if not self.is_debug: # checks whether the unittests are ran
            self.save()
        # changes the status code to 201 Created instead of 200 OK with a message
        return JSONResponse(content="Itemline was succesfully added to the database", status_code=201) 

    def update_item_type(self, item_type_id:int, new_item_type:ItemType):
        """
        Update an existing item type based on its ID, replacing it with new data.

        :param item_type_id: The ID of the item type to update.
        :param new_item_type: The new data to replace the existing item type.
        :return: True if the item type was successfully updated; otherwise, False.
        """
        self.validate_item_type(new_item_type.model_dump())
        if not self.is_debug:
            self.load(self.is_debug)
        # checks whether object isnt null and whether the id is valid
        if self.get_item_type(item_type_id) is None or not self.check_valid_id(item_type_id):
            raise HTTPException(status_code=400,
                                detail="Invalid id or can't find the item type to be updated")

        
        # In the JSON body there is an itemline object sent,
        # with the values that the user desires to change in the old object
        new_itemtype_dict = new_item_type.model_dump()
        new_itemtype_dict["updated_at"] = self.get_timestamp()
        
        # After updating, the system changes the updating date and time,
        # to the date and time when the updating took place.
        for old_itemtype in self.data:
            '''
            the system searches through the database,
            until it finds an object, that matches the id given as a parameter
            '''
            if old_itemtype["id"] == item_type_id:
                old_itemtype.update(new_itemtype_dict)
                if not self.is_debug:
                    self.save()
                '''
                The system replaces all values of the found item type object,
                with the values of the item type object sent as a parameter
                '''
                return {"message": "Item type successfully updated."}
        return {"message: Item time not updated"}

    def remove_item_type(self, item_type_id:int):
        """
        Delete an item type based on its ID.

        :param item_type_id: The ID of the item type to remove.
        :return: True if the item type was successfully removed; otherwise, False.
        """
        if not self.is_debug:
            self.load(self.is_debug)
        if self.get_item_type(item_type_id) is None or not self.check_valid_id(item_type_id):
            raise HTTPException(status_code=400,                              
                                detail=f"Invalid itemline id: {item_type_id} or item line doesnt exist")
        '''
        The method receives a item_line_id of the client object,
        the user desires to delete.
        '''
        for itemline in self.data:
            if itemline["id"] == item_type_id:
                '''
                 The system searches for the itemline object,
                that matches the id given as a parameter.
                '''
                self.data.remove(itemline)
                if not self.is_debug:
                    self.save()
                '''
                if an itemline object is found,
                the system deletes it from the database.
                '''
                return {"message":
                        "itemline successfully removed from the database."}

    def load(self, is_debug):
        """
        Load data from the JSON file or use sample data if in debug mode.

        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        if is_debug:
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
        try:
            with open(self.data_path, "w") as file:
                json.dump(self.data, file, indent=4)
        except(FileNotFoundError, json.JSONDecodeError):
            raise HTTPException(f"{self.data_path} not found or could not be loaded.") 