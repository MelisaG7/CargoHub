import pytest
import httpx

BASE_URL = "http://localhost:3000/api/v1/orders" 

class TestEndpointsOrders:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.headerlist = [
            {"api_key": "a1b2c3d4e5"},
            {"api_key": "f6g7h8i9j0"}
        ]
        self.valid_order_id = 101  # order id
        self.invalid_order_ids = [-1, -20, 1.25, "one hundred"]
        self.new_order = {
            "id": 2021,
            "shipment_id": 500,
            "client_id": 400,
            "items": [
                {"item_id": 1, "amount": 10},
                {"item_id": 2, "amount": 5}
            ],
            "created_at": "2024-01-01 10:00:00",
            "updated_at": "2024-01-02 11:00:00"
        }
        self.partial_order_data = {
            "id": 2022,
            "shipment_id": 501
        }

    def test_get_orders(self):
        response = httpx.get(BASE_URL, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(BASE_URL, headers=self.headerlist[1])
        assert response.status_code == 403  # Verkeerde API-sleutel

    def test_get_order(self):
        response = httpx.get(f"{BASE_URL}/{self.valid_order_id}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.valid_order_id

        for invalid_id in self.invalid_order_ids:
            response = httpx.get(f"{BASE_URL}/{invalid_id}", headers=self.headerlist[0])
            assert response.status_code == 404  # Niet gevonden

        response = httpx.get(f"{BASE_URL}/{self.valid_order_id}", headers=self.headerlist[1])
        assert response.status_code == 403

    def test_post_order(self):
        response = httpx.post(BASE_URL, json=self.new_order, headers=self.headerlist[0])
        assert response.status_code == 201

        response = httpx.get(f"{BASE_URL}/{self.new_order['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.new_order['id']

        response = httpx.post(BASE_URL, json=self.new_order, headers=self.headerlist[1])
        assert response.status_code == 403

        response = httpx.post(BASE_URL, json=self.partial_order_data, headers=self.headerlist[0])
        assert response.status_code == 400  # Slechte aanvraag

    def test_put_order(self):
        updated_order = self.new_order.copy()
        updated_order["items"] = [{"item_id": 1, "amount": 20}]

        response = httpx.put(f"{BASE_URL}/{self.new_order['id']}", json=updated_order, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{self.new_order['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["items"][0]["amount"] == 20

        response = httpx.put(f"{BASE_URL}/{self.new_order['id']}", json=updated_order, headers=self.headerlist[1])
        assert response.status_code == 403

    def test_remove_order(self):
        response = httpx.delete(f"{BASE_URL}/{self.new_order['id']}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{self.new_order['id']}", headers=self.headerlist[0])
        assert response.status_code == 404

        response = httpx.delete(f"{BASE_URL}/{self.new_order['id']}", headers=self.headerlist[1])
        assert response.status_code == 403
