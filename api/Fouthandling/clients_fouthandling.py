

class ClientsFoutHandling:

    def __init__(self):
        self.RequiredFields = [
            "id", "name", "address", "city", 
            "zip_code", "province", "country", 
            "contact_name", "contact_phone",
            "contact_email"
        ]

    def clients():
        from models.clients import Clients
        return Clients("./data/", False)

    def check_valid_id(self, client_id):
        if client_id < 0:
            return False
        return True

    def check_valid_body(self, client):
        for field in self.RequiredFields:
            if field not in client:
                return False
        return True

    def check_get_client(self, client_id):
        # check on negatieve IDs
        return self.check_valid_id(client_id)

    def check_add_client(self, client):
        # Check wheter the sent JSON body matches the body of a client object
        if self.check_valid_body(client):
            # Check whether the ID in the JSON body already exists
            # in the database or not. Voorkom dubbele IDS
            for klant in self.clients().client_database:
                if klant["id"] == client["id"]:
                    return False
            return True
        return False

    def check_put_client(self, client, client_id):
        # Make sure the ID in the JSON body is
        # the same als van de client body die je wilt verandered
        if self.check_valid_body(client):
            if client["id"] == client_id:
                return True
        return False

    def check_remove_client(self, client_id):
        # Check pp negatieve ID's
        return self.check_valid_id(client_id)
