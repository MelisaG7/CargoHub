
import pytest
import httpx

BASE_URL = "http://localhost:3000/api/v1/locations"  # Aanpassen naar jouw server-URL

class TestEndpointsLocations:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.headerlist = [
            {"api_key": "a1b2c3d4e5"},
            {"api_key": "f6g7h8i9j0"}
        ]
        self.valid_location_id = 101  # Een bestaande location ID
        self.invalid_location_ids = [-1, -20, 1.25, "hundred"]
        self.new_location = {
            "id": 2021,
            "warehouse_id": 300,
            "location_name": "Warehouse Section B",
            "total_capacity": 500,
            "occupied_capacity": 150,
            "created_at": "2024-01-01 10:00:00",
            "updated_at": "2024-01-02 11:00:00"
        }
        self.partial_location_data = {
            "id": 2022,
            "warehouse_id": 301,
            "location_name": "Warehouse Section C"
        }

    def test_get_locations(self):
        response = httpx.get(BASE_URL, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(BASE_URL, headers=self.headerlist[1])
        assert response.status_code == 403  # Verkeerde API-sleutel

    def test_get_location(self):
        response = httpx.get(f"{BASE_URL}/{self.valid_location_id}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.valid_location_id

        for invalid_id in self.invalid_location_ids:
            response = httpx.get(f"{BASE_URL}/{invalid_id}", headers=self.headerlist[0])
            assert response.status_code == 404  # Niet-gevonden statuscode

        response = httpx.get(f"{BASE_URL}/{self.valid_location_id}", headers=self.headerlist[1])
        assert response.status_code == 403

    def test_post_location(self):
        response = httpx.post(BASE_URL, json=self.new_location, headers=self.headerlist[0])
        assert response.status_code == 201

        response = httpx.get(f"{BASE_URL}/{self.new_location['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.new_location['id']

        response = httpx.post(BASE_URL, json=self.new_location, headers=self.headerlist[1])
        assert response.status_code == 403

        response = httpx.post(BASE_URL, json=self.partial_location_data, headers=self.headerlist[0])
        assert response.status_code == 400  # Slechte aanvraag (onvolledige data)

    def test_put_location(self):
        updated_location = self.new_location.copy()
        updated_location["occupied_capacity"] = 200

        response = httpx.put(f"{BASE_URL}/{self.new_location['id']}", json=updated_location, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{self.new_location['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["occupied_capacity"] == 200

        response = httpx.put(f"{BASE_URL}/{self.new_location['id']}", json=updated_location, headers=self.headerlist[1])
        assert response.status_code == 403

    def test_remove_location(self):
        response = httpx.delete(f"{BASE_URL}/{self.new_location['id']}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{self.new_location['id']}", headers=self.headerlist[0])
        assert response.status_code == 404

        response = httpx.delete(f"{BASE_URL}/{self.new_location['id']}", headers=self.headerlist[1])
        assert response.status_code == 403
