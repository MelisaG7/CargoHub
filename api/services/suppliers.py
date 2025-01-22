import json
from services.base import Base
from fastapi import APIRouter, HTTPException
from models.Models import Supplier
from fastapi.responses import JSONResponse

SUPPLIERS = []


class Suppliers(Base):
    def __init__(self, root_path, is_debug=False):
        """Initializes the Suppliers class with the path to the JSON file and loads the data.

        Args:
            root_path (str): Base path to the data.
            is_debug (bool): Indicates if debug data should be loaded.
        """
        self.data_path = root_path + "suppliers.json"
        self.is_debug = is_debug
        self.load(is_debug)
        self.router = APIRouter()
        self.router.add_api_route(
            "/suppliers", self.get_suppliers, methods=["GET"])
        self.router.add_api_route(
            "/suppliers/{supplier_id}", self.get_supplier, methods=["GET"])
        self.router.add_api_route(
            "/suppliers/{supplier_id}/items", self.get_items_supplies, methods=["GET"])
        self.router.add_api_route(
            "/suppliers", self.add_supplier, methods=["POST"])
        self.router.add_api_route(
            "/suppliers/{supplier_id}", self.update_supplier, methods=["PUT"])
        self.router.add_api_route(
            "/suppliers/{supplier_id}", self.remove_supplier, methods=["DELETE"])

    def get_suppliers(self):
        """Returns a list of all suppliers stored in the data."""
        return self.data

    def get_supplier(self, supplier_id: int):
        """Finds a specific supplier by ID and returns it as a dictionary.

        Args:
            supplier_id (int): ID of the supplier to retrieve.

        Returns:
            dict: The supplier data if found, otherwise None.
        """
        for supplier in self.data:
            if supplier["id"] == supplier_id:
                return supplier
        return None

    def get_items_supplies(self, supplier_id: int):
        from services.items import Items
        try:
            items_obj = Items("./data/", False)
            items = items_obj.get_items_for_supplier(supplier_id)

            if not items:  # Controleer of de lijst leeg is
                return JSONResponse(content="No items found for the given supplier.", status_code=404)

            return items

        except Exception as e:
            print(e)

    def add_supplier(self, supplier: Supplier):
        """Adds a new supplier to the data with created and updated timestamps.

        Args:
            supplier (dict): The data of the supplier to add.
        """
        supplier_dictionary = supplier.model_dump()
        supplier_dictionary["created_at"] = self.get_timestamp()
        supplier_dictionary["updated_at"] = self.get_timestamp()
        self.data.append(supplier_dictionary)
        if not self.is_debug:
            self.save()
        try:
            return JSONResponse(content="Supplier has been added", status_code=201)
        except Exception as e:
            print(e)

    def update_supplier(self, supplier_id: int, supplier: Supplier):
        """Updates an existing supplier based on the supplier ID.

        Args:
            supplier_id (int): ID of the supplier to update.
            supplier (dict): The updated supplier data.
        """
        supplier_dictionary = supplier.model_dump()
        supplier_dictionary["updated_at"] = self.get_timestamp()
        for suppliers in self.data:
            try:
                if suppliers["id"] == supplier_id:
                    suppliers.update(supplier_dictionary)
                    self.save()
                    return
            except Exception as e:
                print(e)

    def remove_supplier(self, supplier_id: int):
        """Removes a supplier from the data based on the supplier ID.

        Args:
            supplier_id (int): ID of the supplier to remove.
        """
        for supplier in self.data:
            if supplier["id"] == supplier_id:
                self.data.remove(supplier)
        if not self.is_debug:
            self.save()

    def load(self, is_debug):
        if is_debug:
            self.data = SUPPLIERS
        else:
            f = open(self.data_path, "r")
            self.data = json.load(f)
            f.close()

    def save(self):
        f = open(self.data_path, "w")
        json.dump(self.data, f)
        f.close()
