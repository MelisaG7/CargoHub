import pytest
from services.clients import Clients
from fastapi import HTTPException
from models.Models import Client


class TestClients:

    def setup_method(self):
        self.clients = Clients("./data/", is_debug=True)
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
        # a - an existing Id
        Id_A = 20
        # b - a non-existing Id
        Id_B = 10000
        # c - a negative Id
        Id_C = -20
        result_A = self.clients.get_client(Id_A)
        assert result_A == self.clients.client_database[0]

        with pytest.raises(HTTPException):
            self.clients.get_client(Id_B)

        with pytest.raises(HTTPException):
            self.clients.get_client(Id_C)

    def test_add_client(self):
        # 1) geef een juiste client body door aan de methode
        client_body = Client(
            id=30,
            name="Julian Haites",
            address="Somewhere in London 1234 AB",
            city="London",
            zip_code="12345",
            province="The province London lies in",
            country="United Kingdom",
            contact_name="Daisy Haites",
            contact_phone="001-888-777-666-555",
            contact_email="jhaites@example.net"
        )
        # Nu moet ik dus kijken of de client_body daadwerkelijk nu in data zit
        self.clients.add_client(client_body)
        assert self.clients.client_database[-1]["name"] == client_body.name
        assert self.clients.client_database[-1]["id"] == client_body.id

    def test_update_client(self):
        # The user must pass a client object with a matching ID,
        # to that of a client object in the client_databasebase,
        # in order for the system to update that client object.
        new_client_body = Client(
            id=20,
            name="Daisy Haites",
            address="Somwhere in New York, a street 38 12345 HC",
            city="New York",
            zip_code="54321",
            province="The province London lies in",
            country="United States",
            contact_name="Daisy Haites",
            contact_phone="001-888-777-666-555",
            contact_email="dhaites@example.net"
        )

        # Check de methode met de juiste ID en een correct aangepaste body
        self.clients.update_client(20, new_client_body)
        assert self.clients.client_database[0]["id"] == new_client_body.id

        # Nu ga ik checken of het werkt met een verkeerd Id?
        with pytest.raises(HTTPException):
            self.clients.update_client(32, new_client_body)

    def test_delete_client(self):
        result = []
        # Check of de client in de client_databaselijst verwijderd is.
        # Omdat er maar een persoon in zit, kan je checken of de lijst leeg is
        self.clients.remove_client(20)
        assert self.clients.client_database == result
        # Nu gaan we kijken wat er gebeurd als je twee personen
        # met dezelfde Id verwijderd?
        with pytest.raises(HTTPException):
            self.clients.remove_client(20)


if __name__ == '__main__':
    pytest.main()