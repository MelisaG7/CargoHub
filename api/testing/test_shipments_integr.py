import pytest
import httpx

BASE_URL = "http://localhost:3000/api/v1/shipments"  # Pas dit aan naar jouw server-URL

class TestEndpointsShipments:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.headerlist = [
            {"api_key": "a1b2c3d4e5"},
            {"api_key": "f6g7h8i9j0"}
        ]
        self.valid_shipment_id = 101  # shipment ID
        self.invalid_shipment_ids = [-1, -20, 1.25, "hundred"]
        self.new_shipment = {
            "id": 2021,
            "client_id": 300,
            "shipment_date": "2024-01-01 10:00:00",
            "status": "Pending",
            "items": [
                {"item_id": 1, "amount": 50},
                {"item_id": 2, "amount": 20}
            ]
        }

    def test_get_shipments(self):
        response = httpx.get(BASE_URL, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(BASE_URL, headers=self.headerlist[1])
        assert response.status_code == 403  # Verkeerde API-sleutel

    def test_get_shipment(self):
        response = httpx.get(f"{BASE_URL}/{self.valid_shipment_id}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.valid_shipment_id

        for invalid_id in self.invalid_shipment_ids:
            response = httpx.get(f"{BASE_URL}/{invalid_id}", headers=self.headerlist[0])
            assert response.status_code == 404  # Niet-gevonden statuscode

        response = httpx.get(f"{BASE_URL}/{self.valid_shipment_id}", headers=self.headerlist[1])
        assert response.status_code == 403

    def test_post_shipment(self):
        response = httpx.post(BASE_URL, json=self.new_shipment, headers=self.headerlist[0])
        assert response.status_code == 201

        response = httpx.get(f"{BASE_URL}/{self.new_shipment['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.new_shipment['id']

        response = httpx.post(BASE_URL, json=self.new_shipment, headers=self.headerlist[1])
        assert response.status_code == 403

    def test_put_shipment(self):
        updated_shipment = self.new_shipment.copy()
        updated_shipment["status"] = "Shipped"

        response = httpx.put(f"{BASE_URL}/{self.new_shipment['id']}", json=updated_shipment, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{self.new_shipment['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["status"] == "Shipped"

        response = httpx.put(f"{BASE_URL}/{self.new_shipment['id']}", json=updated_shipment, headers=self.headerlist[1])
        assert response.status_code == 403

    def test_remove_shipment(self):
        response = httpx.delete(f"{BASE_URL}/{self.new_shipment['id']}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{self.new_shipment['id']}", headers=self.headerlist[0])
        assert response.status_code == 404

        response = httpx.delete(f"{BASE_URL}/{self.new_shipment['id']}", headers=self.headerlist[1])
        assert response.status_code == 403
