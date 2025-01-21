import pytest
import httpx
import os

# Aanpassen naar jouw server-URL
BASE_URL = "http://localhost:3000/api/v1/locations/"


class TestEndpointsLocations:

    @pytest.fixture(autouse=True)
    def setup(self):
        if not os.getenv("GITHUB_ACTIONS"):
            from dotenv import load_dotenv
            load_dotenv()

        # Laad de API-keys dynamisch uit de omgeving
        self.headerlist = [
            {"api_key": os.getenv("API_KEY_1")},
            {"api_key": os.getenv("API_KEY_3")}]
        # api_key 3 is een foutieve key om te testen op toegankelijkheid
        self.valid_location_id = 101  # Een bestaande location ID
        self.invalid_location_ids = [-1, -20, 1.25, "hundred"]
        self.new_location = {"id": 1, "warehouse_id": 1, "code": "A.1.0", "name": "Row: A, Rack: 1, Shelf: 0",
                             "created_at": "1992-05-15 03:21:32", "updated_at": "1992-05-15 03:21:32"}
        self.partial_location_data = {
            "id": 2022,
            "warehouse_id": 301,
            "location_name": "Warehouse Section C"
        }

    def test_get_locations(self):
        response = httpx.get(BASE_URL, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(BASE_URL, headers=self.headerlist[1])
        assert response.status_code == 401  # Verkeerde API-sleutel

    def test_get_location(self):
        response = httpx.get(
            f"{BASE_URL}{self.valid_location_id}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.valid_location_id

        response = httpx.get(
            f"{BASE_URL}{self.valid_location_id}", headers=self.headerlist[1])
        assert response.status_code == 401

    def test_post_location(self):
        response = httpx.post(
            BASE_URL, json=self.new_location, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(
            f"{BASE_URL}{self.new_location['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.new_location['id']

        response = httpx.post(
            BASE_URL, json=self.new_location, headers=self.headerlist[1])
        assert response.status_code == 401

    def test_put_location(self):
        updated_location = self.new_location.copy()
        updated_location["occupied_capacity"] = 200

        response = httpx.put(
            f"{BASE_URL}{self.new_location['id']}", json=updated_location, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.put(
            f"{BASE_URL}{self.new_location['id']}", json=updated_location, headers=self.headerlist[1])
        assert response.status_code == 401

    def test_remove_location(self):
        response = httpx.delete(
            f"{BASE_URL}{self.new_location['id']}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.delete(
            f"{BASE_URL}{self.new_location['id']}", headers=self.headerlist[1])
        assert response.status_code == 401
