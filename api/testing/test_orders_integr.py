import pytest
import httpx
import os

BASE_URL = "http://localhost:3000/api/v1/orders/"


class TestEndpointsOrders:

    @pytest.fixture(autouse=True)
    def setup(self):
        if not os.getenv("GITHUB_ACTIONS"):
            from dotenv import load_dotenv
            load_dotenv()

        # Laad de API-keys dynamisch uit de omgeving
        self.headerlist = [
            {"api_key": os.getenv("API_KEY_1")},
            {"api_key": os.getenv("API_KEY_3")}
        ]
        # api_key 3 is een foutieve key om te testen op toegankelijkheid
        self.valid_order_id = 101  # order id
        self.invalid_order_ids = [-1, -20, 1.25, "one hundred"]
        self.new_order = {
            "id": 4847,
            "source_id": 46,
            "order_date": "1989-12-01T05:52:40Z",
            "request_date": "1989-12-05T05:52:40Z",
            "reference": "ORD04842",
            "reference_extra": "Zien woud antwoorden comfortabel goedkoop.",
            "order_status": "Shipped",
            "notes": "Oost lach erg geven elektrisch priv\u00e9 foto zoon.",
            "shipping_notes": "Groeien rijk hen elektrisch boek eerste vernietigen.",
            "picking_notes": "Wat langzaam van zou fout bed olifant.",
            "warehouse_id": 17,
            "ship_to": "1299",
            "bill_to": "1299",
            "shipment_id": 9267,
            "total_amount": 5441.9,
            "total_discount": 374.76,
            "total_tax": 566.37,
            "total_surcharge": 26.88,
            "created_at": "1989-12-01T05:52:40Z",
            "updated_at": "1989-12-03T01:52:40Z",
            "items": [
                {
                    "item_id": "P010289",
                    "amount": 48
                },
                {
                    "item_id": "P006554",
                    "amount": 43
                },
                {
                    "item_id": "P011173",
                    "amount": 38
                }
            ]
        }
        self.partial_order_data = {
            "id": 2022,
            "shipment_id": 501
        }

    def test_get_orders(self):
        response = httpx.get(BASE_URL, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(BASE_URL, headers=self.headerlist[1])
        assert response.status_code == 401  # Verkeerde API-sleutel

    def test_get_order(self):
        response = httpx.get(
            f"{BASE_URL}{self.valid_order_id}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.valid_order_id

        response = httpx.get(
            f"{BASE_URL}{self.valid_order_id}", headers=self.headerlist[1])
        assert response.status_code == 401

    def test_post_order(self):
        response = httpx.post(BASE_URL, json=self.new_order,
                              headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.post(BASE_URL, json=self.new_order,
                              headers=self.headerlist[1])
        assert response.status_code == 401

    def test_put_order(self):
        updated_order = self.new_order.copy()
        updated_order["items"] = [{"item_id": 1, "amount": 20}]

        response = httpx.put(
            f"{BASE_URL}{self.new_order['id']}", json=updated_order, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(
            f"{BASE_URL}{self.new_order['id']}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["items"][0]["amount"] == 20

        response = httpx.put(
            f"{BASE_URL}{self.new_order['id']}", json=updated_order, headers=self.headerlist[1])
        assert response.status_code == 401

    def test_remove_order(self):
        response = httpx.delete(
            f"{BASE_URL}{self.new_order['id']}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.delete(
            f"{BASE_URL}{self.new_order['id']}", headers=self.headerlist[1])
        assert response.status_code == 401
