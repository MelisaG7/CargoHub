import pytest
import httpx
import os
from models.Models import Shipment

# Pas dit aan naar jouw server-URL
BASE_URL = "http://localhost:3000/api/v1/shipments/"


class TestEndpointsShipments:
    @pytest.fixture(autouse=True)
    def setup(self):
        if not os.getenv("GITHUB_ACTIONS"):
            from dotenv import load_dotenv
            load_dotenv()

        # Laad de API-keys dynamisch uit de omgeving
        self.headerlist = [
            {"api_key": os.getenv("API_KEY_1")},
            {"api_key": os.getenv("API_KEY_2")}]
        # api_key 3 is een foutieve key om te testen op toegankelijkheid
        self.valid_shipment_id = 101  # shipment ID
        self.invalid_shipment_ids = [-1, -20, 1.25, "hundred"]
        self.new_shipment = {
            "id": 69000,
            "order_id": 690,
            "source_id": 29,
            "order_date": "2006-04-12",
            "request_date": "2006-04-14",
            "shipment_date": "2006-04-16",
            "shipment_type": "I",
            "shipment_status": "Pending",
            "notes": "Lamp pen vuur daarom.",
            "carrier_code": "FedEx",
            "carrier_description": "Federal Express",
            "service_code": "NextDay",
            "payment_type": "Automatic",
            "transfer_mode": "Air",
            "total_package_count": 14,
            "total_package_weight": 392.69,
            "created_at": "2006-04-12T21:30:59Z",
            "updated_at": "2006-04-13T23:30:59Z",
            "items": [
                {
                    "item_id": "P004000",
                    "amount": 22
                },
                {
                    "item_id": "P009257",
                    "amount": 10
                },
                {
                    "item_id": "P010299",
                    "amount": 44
                },
                {
                    "item_id": "P011487",
                    "amount": 49
                }
            ]
        }
        self.new_items =[
            {
                "item_id": "P007435",
                "amount": 23
            },
            {
                "item_id": "P009557",
                "amount": 1
            }
            ]

    def test_get_shipments(self):
        response = httpx.get(
            BASE_URL, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(BASE_URL, headers=self.headerlist[1])
        assert response.status_code == 200 

    def test_get_shipment(self):
        response = httpx.get(f"{BASE_URL}{self.valid_shipment_id}",
                             headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == self.valid_shipment_id

        response = httpx.get(
            f"{BASE_URL}{self.valid_shipment_id}", headers=self.headerlist[1])
        assert response.status_code == 200

    def test_items_in_shipment(self):
        response = httpx.get(f"{BASE_URL}{self.valid_shipment_id}/items",
                             headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(
            f"{BASE_URL}{self.valid_shipment_id}/items", headers=self.headerlist[1])
        assert response.status_code == 200

    def test_post_shipment(self):
        response = httpx.post(
            BASE_URL, json=self.new_shipment, headers=self.headerlist[0])
        assert response.status_code == 201

        response = httpx.post(
            BASE_URL, json=self.new_shipment, headers=self.headerlist[1])
        assert response.status_code == 403

    def test_put_shipment(self):
        updated_shipment = self.new_shipment.copy()
        updated_shipment["status"] = "Shipped"

        response = httpx.put(
            f"{BASE_URL}{4}", json=updated_shipment, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.put(
            f"{BASE_URL}{self.new_shipment['id']}", json=updated_shipment, headers=self.headerlist[1])
        assert response.status_code == 403

    def test_remove_shipment(self):
        response = httpx.delete(
            f"{BASE_URL}{9}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.delete(
            f"{BASE_URL}{2}", headers=self.headerlist[1])
        assert response.status_code == 403
    