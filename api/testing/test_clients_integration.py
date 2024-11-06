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
        self.original_data = self.load_all_client_data()

        yield

        self.teardown()

    def load_all_client_data(self):
        with open('clients.json', 'r') as file:
            return json.load(file)

    def restore_original_data(self):
        with open('clients.json', 'w') as file:
            json.dump(self.original_data, file)

    def load_client_data(self, client_id):
        with open('clients.json', 'r') as file:
            data = json.load(file)
            for client in data["clients"]:
                if client["id"] == client_id:
                    return client
        return None

    def teardown(self):
        self.restore_original_data()

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
            assert response.status_code == 404

    def test_post_client(self):
        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.DummyClient, headers=self.headerlist[0])
        assert response.status_code == 201

        client_data = self.load_client_data(self.DummyClient["id"])
        assert client_data == self.DummyClient

        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.DummyClient, headers=self.headerlist[1])
        assert response.status_code == 403

        response = httpx.post(f"{BASE_URL}/api/v1/clients", json=self.WrongDummyClient, headers=self.headerlist[0])
        assert response.status_code == 400

    def test_put_client(self):
        response = httpx.put(f"{BASE_URL}/api/v1/clients/{1}", json=self.DummyClient, headers=self.headerlist[0])
        assert response.status_code == 200
        updated_client_data = self.load_client_data(1)
        assert updated_client_data["name"] == self.DummyClient["name"]
        assert updated_client_data["city"] == self.DummyClient["city"]

    def test_remove_client(self):
        response = httpx.delete(f"{BASE_URL}/api/v1/clients/{11}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/api/v1/clients/{11}", headers=self.headerlist[0])
        assert response.status_code == 404

        response = httpx.delete(f"{BASE_URL}/api/v1/clients/{12}", headers=self.headerlist[1])
        assert response.status_code == 403

if __name__ == '__main__':
    pytest.main()
