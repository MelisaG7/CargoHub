import json
from services.base import Base
# from models.Models import ItemLine
from fastapi import APIRouter, HTTPException
from models.Models import ItemLine
from fastapi.responses import JSONResponse


class ItemLines(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the ItemLines class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "item_lines.json"
        self.is_debug = is_debug
        self.data = []
        self.required_fields = [
            "id", "name", "description"
        ]
        self.load(is_debug)

        self.router = APIRouter()

        self.router.add_api_route(
            "/item_lines", self.get_item_lines, methods=["GET"])
        self.router.add_api_route(
            "/item_lines/{item_line_id}", self.get_item_line, methods=["GET"])
        self.router.add_api_route(
            "/item_lines", self.add_item_line, methods=["POST"])
        self.router.add_api_route(
            "/item_lines/{item_line_id}", self.update_item_line, methods=["PUT"])
        self.router.add_api_route(
            "/item_lines/{item_line_id}", self.remove_item_line, methods=["DELETE"])

    def check_valid_id(self, item_line_id: int):
        """
        Check if the provided ID is valid (non-negative).

        :param item_line_id: The unique identifier to validate.
        :return: True if the ID is valid, False otherwise.
        """
        return item_line_id >= 0

    def validate_item_line(self, item_line: dict):
        for field in self.required_fields:
            if field not in item_line:
                raise HTTPException(
                    status_code=400, detail=f"Missing required field: {field}")
        return True

    def get_item_lines(self):
        """
        Retrieve all item lines from the JSON data.

        :return: A list of all item line objects.
        """
        return self.data

    def get_item_line(self, item_line_id: int):
        try:
            """
            Retrieve a specific item line based on its ID.

            :param item_line_id: The unique identifier for the item line.
            :return: The item line dictionary if found, otherwise exception message.
            """
            if not self.check_valid_id(item_line_id):
                raise HTTPException(status_code=400,
                                    detail=f"Invalid itemline id: {item_line_id}")

            # Fetches client based on id
            for itemline in self.data:
                if itemline["id"] == item_line_id:
                    '''
                    # if the item was found,
                    # the server returns the found itemline object
                    + 200 ok
                    '''
                    return itemline

            raise HTTPException(status_code=404,
                                detail=f"Itemline with id {item_line_id} was not found")
        except Exception as e:
            print(e)

    def add_item_line(self, item_line: ItemLine):
        """
        Add a new item line to the JSON data with timestamps for creation and update.

        :param item_line: A dictionary representing the new item line to add.
        :return: Message with information about the status of deletion

        """

        item_line_dict = item_line.model_dump()

        # checks whether item_line has the correct body
        self.validate_item_line(item_line_dict)
        if not self.is_debug:
            self.load(self.is_debug)

        # Loops through the existing to data if there already is an item line with the same id
        for line in self.data:
            if line["id"] == item_line_dict["id"]:
                raise HTTPException(
                    status_code=400, detail="There already is a itemline with the same id")

        '''
        # The server adds'created_at' and 'updated_at',
        # with the current date and time.
        '''
        itemline_data = item_line_dict

        itemline_data["created_at"] = self.get_timestamp()
        itemline_data["updated_at"] = self.get_timestamp()

        # The system adds the clientobject to the database
        self.data.append(itemline_data)
        if not self.is_debug:  # checks whether the unittests are ran
            self.save()
        # changes the status code to 201 Created instead of 200 OK with a message
        return JSONResponse(content="Itemline was succesfully added to the database", status_code=201)

    def update_item_line(self, item_line_id: int, new_item_line: ItemLine):
        """
        Update an existing item line with new data, based on its ID.

        :param item_line_id: The unique identifier for the item line to update.
        :param new_item_line: A dictionary containing updated data for the item line.
        :return: Message with information about the status of deletion
        """
        # checks whether item_line has the correct body
        self.validate_item_line(new_item_line.model_dump())
        if not self.is_debug:
            self.load(self.is_debug)
        # checks whether object isnt null and whether the id is valid
        if self.get_item_line(item_line_id) is None or item_line_id < 0:
            raise HTTPException(status_code=400,
                                detail="Invalid itemline id or can't find the itemline to be updated")

        # In the JSON body there is an itemline object sent,
        # with the values that the user desires to change in the old object
        new_itemline_object = new_item_line.model_dump()
        new_itemline_object["updated_at"] = self.get_timestamp()

        # After updating, the system changes the updating date and time,
        # to the date and time when the updating took place.
        for old_itemline in self.data:
            '''
            the system searches through the database,
            until it finds an object, that matches the id given as a parameter
            '''
            if old_itemline["id"] == item_line_id:
                old_itemline.update(new_itemline_object)
                if not self.is_debug:
                    self.save()
                '''
                The system replaces all values of the found itemline object,
                with the values of the itemline object sent as a parameter
                '''
                return {"message": "Itemline successfully updated."}

    def remove_item_line(self, item_line_id: int):
        """
        Remove an item line from the JSON data based on its ID.

        :param item_line_id: The unique identifier for the item line to remove.
        :return: True if the item line was successfully removed; otherwise, False.
        """
        if not self.is_debug:
            self.load(self.is_debug)
        if self.get_item_line(item_line_id) is None or item_line_id < 0:
            raise HTTPException(status_code=400,
                                detail=f"Invalid itemline id: {item_line_id} or item line doesnt exist")
        '''
        The method receives a item_line_id of the client object,
        the user desires to delete.
        '''
        for itemline in self.data:
            if itemline["id"] == item_line_id:
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
        Load item line data from the JSON file, or use sample data if in debug mode.

        :param is_debug: If True, loads sample data instead of data from the JSON file.
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
        """
        Write all current item line data to the JSON file.
        """
        try:
            with open(self.data_path, "w") as file:
                json.dump(self.data, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            raise HTTPException(
                f"{self.data_path} not found or could not be loaded.")
