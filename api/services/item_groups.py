import json
from models.Models import ItemGroup
from services.base import Base
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse


ITEM_GROUPS = []

'''
CHANGES:
Changed 'self.data' to 'self.item_groups_database'
Changed 'self.data_path' to 'self.item_groups_database_path'
Changed 'x' and 'i' to 'item_group'
'''


class ItemGroups(Base):
    def __init__(self, root_path, is_debug=False):
        self.item_groups_database_path = root_path + "item_groups.json"
        self.load(is_debug)
        self.router = APIRouter()

        self.router.add_api_route("/itemgroups", self.get_item_groups, methods=["GET"])
        self.router.add_api_route("/itemgroups/{item_group_id}", self.get_item_group, methods=["GET"])
        self.router.add_api_route("/itemgroups", self.add_item_group, methods=["POST"])
        self.router.add_api_route("/itemgroups/{item_group_id}", self.update_item_group, methods=["PUT"])
        self.router.add_api_route("/itemgroups/{item_group_id}", self.remove_item_group, methods=["DELETE"])

    @staticmethod
    def FoutHandling():
        from Fouthandling.itemgroups_fouthandling import ItemGroupsFoutHandling
        return ItemGroupsFoutHandling()

    def get_item_groups(self):
        # if not self.FoutHandling().check_get_itemgroup
        # returns all item_group objects in the database
        return self.item_groups_database

    def get_item_group(self, item_group_id: int):
        if not self.FoutHandling().check_get_itemgroup(item_group_id):
            raise HTTPException(status_code=400, detail=f"Invalid itemgroup id: {item_group_id}")

        for item_group in self.item_groups_database:
            '''
            The method searches through the database for an
            item_group object that has the same id as the passed id.
            '''
            if item_group["id"] == item_group_id:
                # if there is a match, the found inventory object gets fetched
                return item_group
            '''
            # If nothing was found, it returns 'None' and a 200 status_code.
            # The user sees 'null'
            '''
        raise HTTPException(status_code=404, detail=f"Itemgroup with id: {item_group_id} not found.")

    def add_item_group(self, item_group: ItemGroup):
        if not self.FoutHandling().check_add_itemgroup(item_group):
            raise HTTPException(status_code=400, detail="Invalid item group body.")
        '''
        This method adds/replaces the values of 'created_at' and
        'updated_at' of the passed object to the current date and time
        '''
        item_group_dict = item_group.model_dump()
        item_group_dict["created_at"] = self.get_timestamp()
        item_group_dict["updated_at"] = self.get_timestamp()
        # Then the object gets added to the database
        self.item_groups_database.append(item_group_dict)
        self.save()
        return JSONResponse(status_code=201, content="item group successfully added to the database.")

    def update_item_group(self, item_group_id: int, item_group: ItemGroup):
        if not self.FoutHandling().check_put_itemgroup(item_group, item_group_id):
            raise HTTPException(status_code=400, detail="Invalid item group id or item group body.")
        '''
        This method changes the value of "updated_at"
        of the passed item_group object
        '''
        item_group_dict = item_group.model_dump()
        item_group_dict["updated_at"] = self.get_timestamp()
        for item_groep in self.item_groups_database:
            '''
            Then it searches through the database to an object,
            that has the same id as the one passed
            '''
            if item_groep["id"] == item_group_id:
                '''
                Then it changes the found object,
                to the one passed as a parameter
                '''
                item_groep.update(item_group_dict)
                self.save()
                return JSONResponse(status_code=201, content="item group successfully updated")
        raise HTTPException(status_code=404, detail=f"item group with id: {item_group_id} not found")

    def remove_item_group(self, item_group_id: int):
        if not self.FoutHandling().check_remove_itemgroup(item_group_id):
            raise HTTPException(status_code=400, detail=f"invalid item group id: {item_group_id}")
        '''
        This method searches through the database for an object,
        that has the same id as the one passed
        '''
        for item_group in self.item_groups_database:
            if item_group["id"] == item_group_id:
                '''
                If there is a match,
                the found object gets removed from the database
                '''
                self.item_groups_database.remove(item_group)
                self.save()
                return JSONResponse(status_code=200, content="item group successfully removed from the database.")
        raise HTTPException(status_code=404, content=f"item group with id {item_group_id} not found.")

    def load(self, is_debug):
        if is_debug:
            self.item_groups_database = ITEM_GROUPS
        else:
            f = open(self.item_groups_database_path, "r")
            self.item_groups_database = json.load(f)
            f.close()

    def save(self):
        f = open(self.item_groups_database_path, "w")
        json.dump(self.item_groups_database, f)
        f.close()
