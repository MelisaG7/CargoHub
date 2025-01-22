import json
from services.base import Base
from services.locations import Locations
from fastapi import APIRouter, HTTPException
from models.Models import Warehouse
from fastapi.responses import JSONResponse

WAREHOUSES = []


class Warehouses(Base):
    def __init__(self, root_path, is_debug=False):
        """
        Initialize the Warehouses class, setting the path to the JSON data file and loading data.

        :param root_path: The root file path to locate the JSON file.
        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        self.data_path = root_path + "warehouses.json"
        self.load(is_debug)
        self.router = APIRouter()
        self.router.add_api_route(
            "/warehouses", self.get_warehouses, methods=["GET"])
        self.router.add_api_route(
            "/warehouses/{warehouse_id}", self.get_warehouse, methods=["GET"])
        self.router.add_api_route(
            "/warehouses/{warehouse_id}/locations", self.get_locations_warehouse, methods=["GET"])
        self.router.add_api_route(
            "/warehouses", self.add_warehouse, methods=["POST"])
        self.router.add_api_route(
            "/warehouses/{warehouse_id}", self.update_warehouse, methods=["PUT"])
        self.router.add_api_route(
            "/warehouses/{warehouse_id}", self.remove_warehouse, methods=["DELETE"])

    def get_warehouses(self):
        # Retrieve all warehouse objects from the JSON file.
        # self.data is a list of all warehouse objects.
        return self.data

    def get_warehouse(self, warehouse_id: int):
        # Retrieve a specific warehouse object based on its ID.
        # Warehouse_id: The ID of the warehouse to retrieve.
        # Returns the warehouse if found, else it returns None.

        for warehouse in self.data:
            if warehouse["id"] == warehouse_id:
                return warehouse
        return None

    def get_locations_warehouse(self, warehouse_id: int):
        try:
            location_obj = Locations("./data/", False)
            return location_obj.get_locations_in_warehouse(warehouse_id)
        except Exception as e:
            print(e)

    def add_warehouse(self, warehouse: Warehouse):
        """
        Add a new warehouse object to the JSON data, setting timestamps for creation and update.

        :param warehouse: The dictionary representing the new warehouse to add.
        """
        warehousedict = warehouse.model_dump()
        warehousedict["created_at"] = self.get_timestamp()
        warehousedict["updated_at"] = self.get_timestamp()
        self.data.append(warehousedict)
        self.save()
        try:
            return JSONResponse(content="Warehouse has been added", status_code=201)
        except Exception as e:
            print(e)

    def update_warehouse(self, warehouse_id: int, warehouse: Warehouse):
        """
        Update an existing warehouse based on its ID, replacing it with new data.

        :param warehouse_id: The ID of the warehouse to update.
        :param warehouse: The new data to replace the existing warehouse.
        :return: True if the warehouse was successfully updated; otherwise, False.
        """
        warehousedict = warehouse.model_dump()
        warehousedict["updated_at"] = self.get_timestamp()
        for warehouses in self.data:
            try:
                if warehouses["id"] == warehouse_id:
                    warehouses.update(warehousedict)
                    self.save()
            except Exception as e:
                print(e)

    def remove_warehouse(self, warehouse_id: int):
        """
        Delete a warehouse based on its ID.

        :param warehouse_id: The ID of the warehouse to remove.
        :return: True if the warehouse was successfully removed; otherwise, False.
        """
        try:
            for warehouse in self.data:
                if warehouse["id"] == warehouse_id:
                    self.data.remove(warehouse)
                    self.save()
        except Exception as e:
            print(e)

    def load(self, is_debug):
        """
        Load data from the JSON file or use sample data if in debug mode.

        :param is_debug: If True, loads sample data instead of data from the JSON file.
        """
        if is_debug:
            self.data = WAREHOUSES
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
