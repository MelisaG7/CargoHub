import pytest
from models.clients import Clients


class TestClients:

    def setup_method(self):
        self.clients = Clients("", True)
        self.clients.client_database = [
            {
                "id": 20,
                "name": "Martin-Nguyen",
                "address": "86546 Boone Plaza Suite 135",
                "city": "North Triciaview",
                "zip_code": "09824",
                "province": "Arizona",
                "country": "United States",
                "contact_name": "Nicole Wilson",
                "contact_phone": "001-706-949-4787x230",
                "contact_email": "margaretbray@example.net",
                "created_at": "1982-06-12 15:25:45",
                "updated_at": "2004-09-22 08:30:53"
            }
        ]

    def test_get_client(self):
        # a - een bestaande Id
        Id_A = 20
        # b - een niet-bestaande Id
        Id_B = 10000
        # c - een negatieve Id
        Id_C = -20
        result_A = self.clients.get_client(Id_A)
        assert result_A == self.clients.client_database[0]

        result_B = self.clients.get_client(Id_B)
        assert result_B is None

        result_C = self.clients.get_client(Id_C)
        assert result_C is None

    def test_add_client(self):
        # 1) geef een juiste client body door aan de methode
        client_body = {
            "id": 30,
            "name": "Julian Haites",
            "address": "Somewhere in London 1234 AB",
            "city": "London",
            "zip_code": "12345",
            "province": "The province London lies in",
            "country": "United Kingdom",
            "contact_name": "Daisy Haites",
            "contact_phone": "001-888-777-666-555",
            "contact_email": "jhaites@example.net"
        }

        # wordt een client object met verkeerde of missende informatie ook ingezet?
        # Ik heb de zip code weggehaald
        wrong_client_body = {
            "id": 25,
            "name": "BJ Ballentine",
            "address": "Somewhere in London 1234 AB",
            "city": "London",
            "province": "The province London lies in",
            "country": "United Kingdom",
            "contact_name": "Magnolia Parks",
            "contact_phone": "001-888-777-666-555",
            "contact_email": "BeejnParks@example.net"
        }
        # Wat gebeurd er als ik een lege body doorgeef?
        empty_client_body = {}
        # Nu moet ik dus kijken of de client_body daadwerkelijk nu in data zit
        self.clients.add_client(client_body)
        assert self.clients.client_database[-1] == client_body

        self.clients.add_client(empty_client_body)
        assert self.clients.client_database[-1] != empty_client_body 
        # FOUT DETECTED!! Een lege body sturen werkt WEL!

        self.clients.add_client(wrong_client_body)
        assert self.clients.client_database[-1] != wrong_client_body
        # FOUT DETECTED!!! Client objects met missende informatie komen WEL bij alle client_database
    
    def test_update_client(self):
        # The user must pass a client object with a matching ID to that of a client object in the client_databasebase,
        # in order for the system to update that client object.
        new_client_body = {
            "id": 30,
            "name": "Julian Haites",
            "address": "Somwhere in New York, a street 38 12345 HC",
            "city": "New York",
            "zip_code": "54321",
            "province": "The province London lies in",
            "country": "United States",
            "contact_name": "Daisy Haites",
            "contact_phone": "001-888-777-666-555",
            "contact_email": "dhaites@example.net"
        }

        # Check de methode met de juiste ID en een correct aangepaste body
        self.clients.update_client(20, new_client_body)
        assert self.clients.client_database[0]["id"] == new_client_body["id"]

        # Nu ga ik checken of het werkt met een verkeerd Id?
        result = self.clients.update_client(32, new_client_body)
        assert result == None

    def test_delete_client(self):
        result = []
        # Check of de client in de client_databaselijst verwijderd is.
        # Omdat er maar een persoon in zit, kan je checken of de lijst leeg is
        self.clients.remove_client(20)
        assert self.clients.client_database == result
        # Nu gaan we kijken wat er gebeurd als je twee personen met dezelfde Id verwijderd?
        Added_body = {
            "id": 22,
            "name": "Julian Haites",
            "address": "Somwhere in New York, a street 38 12345 HC",
            "city": "New York",
            "zip_code": "54321",
            "province": "The province London lies in",
            "country": "United States",
            "contact_name": "Daisy Haites",
            "contact_phone": "001-888-777-666-555",
            "contact_email": "dhaites@example.net"  
        }
        Added_body2 = {
            "id": 22,
            "name": "Daisy Haites",
            "address": "Somwhere in New York, a street 38 12345 HC",
            "city": "New York",
            "zip_code": "54321",
            "province": "The province London lies in",
            "country": "United States",
            "contact_name": "Daisy Haites",
            "contact_phone": "001-888-777-666-555",
            "contact_email": "dhaites@example.net"
        }
        self.clients.add_client(Added_body)
        self.clients.add_client(Added_body2)
        self.clients.remove_client(22)
        assert self.clients.client_database.__len__() == 1
        # FOUT DETECTED!!!! Ten eerste kan je verschillende clients met dezelfde Id toevoegen,
        # Ten tweede als een deletion wort gerequest, wordt alleen de eerste client met die Id verwijderd.
        # The system shall delete a client object, when given an existing


if __name__ == '__main__':
    pytest.main()
