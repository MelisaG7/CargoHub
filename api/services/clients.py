import json
from services.base import Base
from models.Models import Client
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

CLIENTS = []

'''
CHANGES:
Changed the name 'self.data' to 'self.client_database'
Changed 'self.data_path' to 'self.client_database_path'
Changed variables 'x' and 'i' to 'client'
'''


class Clients(Base):
    def __init__(self, root_path, is_debug=False):
        self.client_database_path = root_path + "clients.json"
        self.is_debug = is_debug
        self.load(is_debug)
        # Voeh je router toe in de init.
        self.router = APIRouter()

        # Oke hier gaan we basically endpoints maken.
        # Elke endpoint heeft zijn eigen CRUD functie ne end-point methode.

        # Vgm hoef ik hier niet veel uit te leggen,
        # doe dit gwn voor elke endpoint die je hebt
        self.router.add_api_route(
            "/clients", self.get_clients, methods=["GET"])
        self.router.add_api_route(
            "/clients/{client_id}", self.get_client, methods=["GET"])
        self.router.add_api_route(
            "/clients", self.add_client, methods=["POST"])
        self.router.add_api_route(
            "/clients/{client_id}", self.update_client, methods=["PUT"])
        self.router.add_api_route(
            "/clients/{client_id}", self.remove_client, methods=["DELETE"])

        # Enn that was it. Je hoeft nu alleen fouthandling toe te voegen,
        # HTTPexceptions en MODEL_DUMP() GEBRUIKEN!!!!
        # (wnr je dingen gaat doen in database)

    @staticmethod
    def FoutHandling():
        from Fouthandling.clients_fouthandling import ClientsFoutHandling
        return ClientsFoutHandling()

    def get_clients(self):
        # Fetches all client objects from the database
        return (self.client_database)

    def get_client(self, client_id: int):
        if not self.FoutHandling().check_get_client(client_id):
            raise HTTPException(status_code=400,
                                detail=f"Invalid client id: {client_id}")

        # Fetches client based on id
        for client in self.client_database:
            if client["id"] == client_id:
                '''
                # if the client was found,
                # the server returns the found client object
                + 200 ok
                '''
                return client

        raise HTTPException(status_code=404,
                            detail=f"Client with id {client_id} was not found")

    def add_client(self, client: Client):
        if not self.FoutHandling().check_add_client(client, self):
            raise HTTPException(status_code=400, detail="Invalid client body")
        # Adds a client object from the database.
        # This method receives a client object as a parameter
        # if not then 422 response

        '''
        # The server adds/replaces the 'created_at' and 'updated_at',
        # with the current date and time.
        '''
        # NIET VERGETEN JE CLIENT OM TE ZETTEN NAAR DICT
        # USE MODEL_DUMP()!!!!
        client_data = client.model_dump()
        client_data["created_at"] = self.get_timestamp()
        client_data["updated_at"] = self.get_timestamp()
        # The system adds the clientobject to the database
        self.client_database.append(client_data)
        self.save()
        return JSONResponse(status_code=201, content={"message": "Client was succesfully added to the database"})

    def update_client(self, client_id: int, client: Client):
        if not self.FoutHandling().check_put_client(client, client_id):
            raise HTTPException(status_code=400,
                                detail="Invalid client id or body.")
        # The server receives a client id and a client object as a JSON body.'
        '''
        The client id is the id of a client object,
        from the database that the user desires to update
        '''

        '''
        In the JSON body there is a client object sent,
        with the values that the user desires to change in the old object
        '''
        client_data = client.model_dump()
        client_data["updated_at"] = self.get_timestamp()
        '''
        After updating, the system changes the updating date and time,
        to the date and time when the updating took place.
        '''
        for klant in self.client_database:
            '''
            the system searches through the database,
            until it finds an object,that matches the id given as a parameter
            '''
            if klant["id"] == client_id:
                klant.update(client_data)
                '''
                The system replaces all values of the found client object,
                with the values of the client object sent as a parameter
                '''
                self.save()
                return {"message": "client successfully updated."}

    def remove_client(self, client_id: int):
        if not self.FoutHandling().check_remove_client(client_id):
            raise HTTPException(status_code=400,
                                detail=f"Invalid client id: {client_id}")
        '''
        The method receives a client_id of the client object,
        the user desires to delete.
        '''
        for client in self.client_database:
            if client["id"] == client_id:
                '''
                The system searches for the client object,
                that matches the id given as a parameter.
                '''
                self.client_database.remove(client)
                '''
                if a client object is found,
                the system deletes it from the database.
                '''
                self.save()
                return {"message": "client successfully removed from the database."}
        raise HTTPException(status_code=404,
                            detail=f"Client with id {client_id} was not found")

    def load(self, is_debug):
        '''
        This method initializes self.client_database
        as the json client database
        '''
        if is_debug:
            self.client_database = CLIENTS
        else:
            f = open(self.client_database_path, "r")
            self.client_database = json.load(f)
            f.close()

    def save(self):
        #  This method saves all changes made in the database
        f = open(self.client_database_path, "w")
        json.dump(self.client_database, f)
        f.close()
