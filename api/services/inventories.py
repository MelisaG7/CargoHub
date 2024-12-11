import json
from models.Models import Inventory
from services.base import Base
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse

INVENTORIES = []

'''
CHANGES:
Changed 'self.data' to 'self.inventory_database'
Changed 'self.data_path' to 'self.inventory_database_path'
Changed 'x' and 'i' to 'inventory'
Changed 'result' to 'found_inventories' (get_inventories_for_item)
Changed 'result' to 'inventory_totals' (get_inventory_totals_for_item)
'''


class Inventories(Base):
    def __init__(self, root_path, is_debug=False):
        self.inventory_database_path = root_path + "inventories.json"
        self.load(is_debug)
        self.router = APIRouter()

        self.router.add_api_route("/inventories", self.get_inventories, methods=["GET"])
        self.router.add_api_route("/inventories/{inventory_id}", self.get_inventory, methods=["GET"])
        self.router.add_api_route("/inventories", self.add_inventory, methods=["POST"])
        self.router.add_api_route("/inventories/{inventory_id}", self.update_inventory, methods=["PUT"])
        self.router.add_api_route("/inventories/{inventory_id}", self.remove_inventory, methods=["DELETE"])

    @staticmethod
    def FoutHandling():
        from Fouthandling.inventories_fouthandling import InventoriesFoutHandling
        return InventoriesFoutHandling()

    def get_inventories(self):
        # This method returns all inventory objects in the database
        return self.inventory_database

    def get_inventory(self, inventory_id: int):
        if not self.FoutHandling().check_get_inventory(inventory_id):
            raise HTTPException(status_code=400, detail=f"Invalid id: {inventory_id}")
        '''
        This method receives an inventory_id
        and searches for a method that has a matching id
        '''
        for inventory in self.inventory_database:
            if inventory["id"] == inventory_id:
                '''
                if an inventory object is found,
                the method returns that object
                '''
                return inventory
            '''
            If nothing was found, the method returns 'None'.
            The user receives a 200 status code and a 'null',
            written in the terminal
            '''
        raise HTTPException(status_code=404, detail=f"Inventory with id {inventory_id} not found in the database")

    # Hahah vergeten welke endpoint ik nodig heb voor dit + geen fouthandling geimplementeerd
    # Ewa ja
    def get_inventories_for_item(self, item_id: int):
        # Skip deze fouthandling voor even want wordt toch even overgeslagen
        # This method searches for inventory objects with item_id
        found_inventories = []
        for inventory in self.inventory_database:
            '''
            the inventories that contain a matching item_id,
            get put in the result list
            '''
            if inventory["item_id"] == item_id:
                found_inventories.append(inventory)
                # the list gets returned
        return found_inventories

    # Nog niet de tijd om deze methods te facen, probs morgen
    def get_inventory_totals_for_item(self, item_id: int):
        # Skip deze ook
        '''
         A dictionary is made for the total of items in inventories
        with a matching item id
        '''
        inventory_totals = {
            "total_expected": 0,
            "total_ordered": 0,
            "total_allocated": 0,
            "total_available": 0
        }
        for inventory in self.inventory_database:
            # The system goes through the database
            if inventory["item_id"] == item_id:
                '''
                # if the system finds an inventory object,
                # with a matching item_id
                # it adds the totals of that item to the values 
                # of the result keys
                '''
                for key in [
                    "total_expected",
                    "total_ordered",
                    "total_allocated",
                    "total_available"
                ]:
                    inventory_totals[key] += inventory[key]
                # Then the method returns the totals/result dictionary
        return inventory_totals

    def add_inventory(self, inventory: Inventory):
        if not self.FoutHandling().check_add_inventory(inventory):
            raise HTTPException(status_code=400, detail="Invalid inventory body")
        '''
        This method adds/replaces the value of the 'created_at' and
        "updated_at" keys with the current date and time.
        '''
        inventory_dict = inventory.model_dump()
        inventory_dict["created_at"] = self.get_timestamp()
        inventory_dict["updated_at"] = self.get_timestamp()
        # After doing so, it adds the passed inventory object to the database
        self.inventory_database.append(inventory_dict)
        self.save()
        return JSONResponse(status_code=201, content="Inventory successfully added to the database")

    def update_inventory(self, inventory_id: int, inventory: Inventory):
        if not self.FoutHandling().check_put_inventory(inventory, inventory_id):
            raise HTTPException(status_code=400, detail="Invalid id or inventory body")
        '''
        The method replaces/adds the value of 'updated_at' of the
        passed inventory object with the current date and time 
        '''
        # Nakijken of dit ook echt werkt btw
        inventory.model_dump()["updated_at"] = self.get_timestamp()
        for inventaris in self.inventory_database:
            # It loops through the database
            if inventaris["id"] == inventory_id:
                '''
                if an inventory object was found with a matching id,
                it replaces all values, with the values of
                the passed inventory object. It replaces the entire object.
                '''
                inventaris.update(inventory.model_dump())
                self.save()
                return JSONResponse(status_code=200, content="inventory succesfully updated")

    def remove_inventory(self, inventory_id: int):
        try:
            if not self.FoutHandling().check_remove_inventory(inventory_id):
                raise HTTPException(status_code=400, detail="Invalid inventory id")
            for inventory in self.inventory_database:
                # The method loops through the database in search of an object
                # that contains the same id as the one passed as a paramter
                if inventory["id"] == inventory_id:
                    # Then it deletes the found inventory object
                    self.inventory_database.remove(inventory)
                    self.save()
                    return JSONResponse(status_code=200, content="Inventory successfully removed from the database")
        except Exception as e:
            print(e)    

    def load(self, is_debug):
        if is_debug:
            self.inventory_database = INVENTORIES
        else:
            f = open(self.inventory_database_path, "r")
            self.inventory_database = json.load(f)
            f.close()

    def save(self):
        f = open(self.inventory_database_path, "w")
        json.dump(self.inventory_database, f)
        f.close()
