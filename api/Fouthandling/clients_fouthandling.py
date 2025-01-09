# Importeer de object uit de folder models, uit de bestand model
# Ik heb alle objecten in een bestand in de folder 'models' gestopt

# De services aka CRUD methodes, zitten in de folder 'services'

# Hierdoor moet je al je imports veranderen (sorry guys)
from models.Models import Client
# Ik heb zoals eerder gezegd in clinets.py,
# al alle objecten voor jullie gemaakt
# Dus dan moet je alleen nog importeren
# No probs!


class ClientsFoutHandling:

    def __init__(self):
        self.RequiredFields = [
            "id", "name", "address", "city", 
            "zip_code", "province", "country", 
            "contact_name", "contact_phone",
            "contact_email"
        ]

    def clients(self, client):
        return client

    def check_valid_id(self, client_id):
        if client_id < 0:
            return False
        return True

    def check_get_client(self, client_id):
        # check on negatieve IDs
        return self.check_valid_id(client_id)

    def check_add_client(self, client: Client, clients):
        # Je hoeft niet meer te checken of de body klopt.
        # Dat doet fastAPI zelf al.
        for klant in clients.client_database:
            # BELANGRIJK! Bij het loopen moet je de client object,
            # eerst omzetten in een dictionary door 'model_dump()' te
            # gebruiken.
            # Als je dat niet doet krijg je een 500 internal server error 
            if klant["id"] == client.model_dump()["id"]:
                return False
        return True

    def check_put_client(self, client: Client, client_id):
        # Make sure the ID in the JSON body is
        # the same als van de client body die je wilt verandered

        # !!Hier ook model_dump() gebruiken,
        # oftwel client object omzetten in een dictionary
        if client.model_dump()["id"] == client_id:
            return True
        return False

    def check_remove_client(self, client_id):
        # Check pp negatieve ID's
        return self.check_valid_id(client_id)