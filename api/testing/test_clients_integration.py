import pytest
import httpx
import json

BASE_URL = "http://localhost:3000"


class TestEndpointsClients:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
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
            "contact_email": "steeletakeshi@example.net"
        }
        self.WrongDummyClient = {
            "id": 9822,
            "name": "Khalani Kanes",
            "address": "Cellblock 7, Braderhelm Prison",
            "city": "Apollo"
        }
        self.original_data = self.load_all_client_data()

        yield

        self.teardown()

    def load_all_client_data(self):
        with open('data/clients.json', 'r') as file:
            return json.load(file)

    def restore_original_data(self):
        with open('data/clients.json', 'w') as file:
            json.dump(self.original_data, file)

    def load_client_data(self, client_id):
        with open('data/clients.json', 'r') as file:
            data = json.load(file)
            for client in data:
                if str(client["id"]) == str(client_id):  # Handle missing "id" key
                    return client
        return None  # Return None if no match is found

    def teardown(self):
        self.restore_original_data()

    def test_get_clients(self):
        response = httpx.get(f"{BASE_URL}/api/v1/clients", headers=self.headerlist[0])
        assert response.status_code == 200
        response = httpx.get(f"{BASE_URL}/api/v1/clients", headers=self.headerlist[1])
        assert response.status_code == 200
        # Dit werkt volledig

    def test_get_client(self):
        # Test for existing IDs
        # for Id in self.ids:
        #     response = httpx.get(f"{BASE_URL}/api/v1/clients/{Id}", headers=self.headerlist[0])
        #     assert response.status_code == 200
        #     assert response.json()["id"] == Id
        
        # Test een id van een object die ik voorheen heb verwijderd:
        httpx.delete(f"{BASE_URL}/api/v1/clients/{1}", headers=self.headerlist[0])
        response = httpx.get(f"{BASE_URL}/api/v1/clients/{1}", headers=self.headerlist[0])
        assert response.status_code == 404

        # Test for non-existing IDs
        for Id in self.WrongIds:
            response = httpx.get(f"{BASE_URL}/api/v1/clients/{Id}", headers=self.headerlist[0])
            assert response.status_code == 400 or response.status_code == 422
            # Oke dus ookal vind het geen clients, het geeft alsnog 200.
    # Deze functie werkt ook volledig

    def test_post_client(self):
        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.DummyClient, headers=self.headerlist[0])
        assert response.status_code == 201

        client_data = self.load_client_data(self.DummyClient["id"])
        assert client_data["name"] == self.DummyClient["name"]
        # Dit werkt

        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.DummyClient, headers=self.headerlist[1])
        assert response.status_code == 403
        # Dit werkt

        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.WrongDummyClient, headers=self.headerlist[0])
        assert response.status_code == 422
        # Fout dummy wordt toch naar de database toegevoegd, ookal mist het. Dus geen fouthandling
    # Deze methode werkt ook naar behoren

    def test_put_client(self):
        response = httpx.put(f"{BASE_URL}/api/v1/clients/{9821}", json=self.DummyClient, headers=self.headerlist[0])
        assert response.status_code == 200
        updated_client_data = self.load_client_data(9821)
        assert updated_client_data["name"] == self.DummyClient["name"]
        assert updated_client_data["city"] == self.DummyClient["city"]
        # Omdat de id van onze dummyclient anders is, wordt ook de client met nummer 1 veranderd naar nummer 9821
        # Hierdoor wordt id 1 verwijderde en bestaat er geen klant object met nummer 1 als id
        # Ik krijg wel een error dat json functie niet gevonden ids niet goed behandeld, will fix that though
        # In principe werkt dit ook volledig

    def test_remove_client(self):
        response = httpx.delete(f"{BASE_URL}/api/v1/clients/{1}", headers=self.headerlist[0])
        assert response.status_code == 200
        # Ik heb even geen idee warrom de status code 500 is ipv van 200. Dit is ook zo bij Thunder
        response = httpx.get(f"{BASE_URL}/api/v1/clients/{1}", headers=self.headerlist[0])
        assert response.status_code == 404
        # Dit is ook 500. De server geeft normaal 200 en dan een 'null' als een object niet kan worden gevonden. Heel raar

        response = httpx.delete(f"{BASE_URL}/api/v1/clients/{12}", headers=self.headerlist[1])
        assert response.status_code == 403
        # Oke dit werkt wel gewoon...maar dit doet niks met verwijderen daarom


if __name__ == '__main__':
    pytest.main()