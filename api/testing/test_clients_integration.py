import pytest
import httpx
import json 

BASE_URL = "http://localhost:3000"  # Vervang dit door de URL van je eigen server


class TestEndpointsClients:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.headerlist = [
            {
                "api_key": "a1b2c3d4e5"
            },
            {
                "api_key": "f6g7h8i9j0"
            }
        ]
        self.ids = [1, 20, 50, 100]
        self.WrongIds = [-1, -20, "hundred"]
        self.DummyClient = {
            "id": 9821,
            "name": "Takeshi Steele",
            "address": "guardquarters, Braderhelm Prison",
            "city": "Apollo",
            "zip_code": "28301",
            "province": "Earth",
            "country": "Stateless",
            "contact_name": "Takeshi Steele",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "steeletakeshi@example.net",
            "created_at": "2010-04-28 02:22:53",
            "updated_at": "2022-02-09 20:22:35"
        }
        self.WrongDummyClient = {
           "id": 317,
           "name": "Khalani Kanes",
           "address": "Cellblock 7, Braderhelm Prison",
           "city": "Apollo"
        }

    def load_client_data(self, client_id):
        with open('clients.json', 'r') as file:
            data = json.load(file)
            for client in data["clients"]:
                if client["id"] == client_id:
                    return client
        return None

    def test_get_clients(self):
        response = httpx.get(f"{BASE_URL}/api/v1/clients", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/api/v1/clients", headers=self.headerlist[1])
        assert response.status_code == 403

    def test_get_client(self):
        # Test for existing IDs
        for Id in self.ids:
            response = httpx.get(f"{BASE_URL}/api/v1/clients/{Id}", headers=self.headerlist[0])
            assert response.status_code == 200
            assert response.json()["id"] == Id

        # Test for non-existing IDs
        for Id in self.WrongIds:
            response = httpx.get(f"{BASE_URL}/api/v1/clients/{Id}", headers=self.headerlist[0])
            assert response.status_code == 404  # Typically 404 for non-existent resource
            # Uhmmm....de respons is by slechte ids gewoon....200?
            # Oke dat komt omdat ik als ik een invalid ID krijg dan krijg ik op de scherm 'null' te zien ipv een bad request.
            # Ik denk dat dat komt omdat de methodes een None returnen wanneer er niks wordt gevonden ipv badrequest

    def test_post_client(self):
        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.DummyClient, headers=self.headerlist[0])
        assert response.status_code == 201
        response = httpx.post(f"{BASE_URL}api/v1/clients/{self.DummyClient["id"]}", headers=self.headerlist[0])
        assert response.status_code == 200

        response == httpx.post(f"{BASE_URL}/api/v1/clients", json=self.DummyClient, headers=self.headerlist[1])
        assert response.status_code == 403
        # ...Wat? Waarom geeft het 201 als het de andere api_key is?

        # Nu moet ik een selchte body creeren om te kijken of die alsnog wordt geaccepteerd.
        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.WrongDummyClient, headers=self.headerlist[0])
        assert response.status_code == 400
        # Yep deze is 201 zoals verwacht
    
    def test_put_client(self):
        response = httpx.put(f"{BASE_URL}/api/v1/clients/{1}", json=self.DummyClient, headers=self.headerlist[0])
        assert response.status_code == 200
        response = httpx.put(f"{BASE_URL}/api/v1/clients/{1}", headers=self.headerlist[0])
        assert response.json()["name"] == self.DummyClient["name"]
        assert response.json()["city"] == self.DummyClient["city"]
        # Ik moet nog hier checken of het daadwerkelijk veranderd is maar op dit moment ben ik helemaal klaar met testen
    
    def test_remove_client(self):
        response = httpx.delete(f"{BASE_URL}/api/v1/clients/{11}", headers=self.headerlist[0])
        assert response.status_code == 200
        # Uh....Ik krijg response 500 ipv 200, maar als ik het handmatig test krijg ik gewoon...200?
        # Vgm omdat mijn slimme hoofd 'httpx.put' deed ipv 'httpx.delete'

        # Checken of id 11 idd uit de json database is
        response = httpx.get(f"{BASE_URL}/api/v1/{11}", headers=self.headerlist[0])
        assert response.status_code == 404
        # API_KEY 2 hoort niet te kunnen deleten
        response = httpx.delete(f"{BASE_URL}/api/v1/clients/{12}", headers=self.headerlist[1])
        assert response.status_code == 403

        # Kijken of het null is of niet ofzo. Of 404 not found, maar deze domme code geeft geen 404 maar gewoon null als input

if __name__ == '__main__':
    pytest.main()
