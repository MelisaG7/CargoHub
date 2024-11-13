import json
# from Fouthandling.clients_fouthandling import ClientsFoutHandling
from models.base import Base

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
        self.load(is_debug)

    def FoutHandling(self):
        from Fouthandling.clients_fouthandling import ClientsFoutHandling
        return ClientsFoutHandling

    def get_clients(self):
        # Fetches all client objects from the database
        return self.client_database

    def get_client(self, client_id):
        # Fetches client based on id
        if not self.FoutHandling().check_get_client(client_id):
            return f"invalid client id: {client_id}"
        for client in self.client_database:
            if client["id"] == client_id:
                '''
                # if the client was found,
                # the server returns the found client object
                '''
                return client
            # If nothing was found, the server returns 'None'.
            # The user will see 'null' on their screen.
        return None
    # In both cases the method returns a 200 status code

    def add_client(self, client):
        # Adds a client object from the database.
        # This method receives a client JSON body as a parameter

        '''
        # The server adds/replaces the 'created_at' and 'updated_at',
        # with the current date and time.
        '''
        client["created_at"] = self.get_timestamp()
        client["updated_at"] = self.get_timestamp()
        # The system adds the clientobject to the database
        self.client_database.append(client)
        # There is no fouthandling though, in none of the methods.

    def update_client(self, client_id, client):
        # The server receives a client id and a client object as a JSON body.'
        '''
        The client id is the id of a client object,
        from the database that the user desires to update
        '''

        '''
        In the JSON body there is a client object sent,
        with the values that the user desires to change in the old object
        '''
        client["updated_at"] = self.get_timestamp()
        '''
        After updating, the system changes the updating date and time,
        to the date and time when the updating took place.
        '''
        for client in range(len(self.client_database)):
            '''
            the system searches through the database,
            until it finds an object,that matches the id given as a parameter
            '''
            if self.client_database[client]["id"] == client_id:
                self.client_database[client] = client
                '''
                The system replaces all values of the found client object,
                with the values of the client object sent as a parameter
                '''
                break

    def remove_client(self, client_id):
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
