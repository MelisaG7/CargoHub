import httpx
import os

BASE_URL = "http://localhost:3000/api/v1"


def test_get_transfers():
    headers = {
        "api_key": "a1b2c3d4e5"
    }
    response = httpx.get(f"{BASE_URL}/transfers", headers=headers)
    assert response.status_code == 200


def test_get_one_transfers():
    api_key = os.getenv("API_KEY_1")
    headers = {
        "api_key": api_key
    }
    response = httpx.get(f"{BASE_URL}/transfers/10", headers=headers)
    assert response.json()["reference"] == "TR00010"
    assert response.status_code == 200


def test_add_transfers():
    headers = {
        "api_key": "a1b2c3d4e5"
    }
    new_transfer = {
        "id": 800000,
        "reference": "TR800000",
        "transfer_from": 5277,
        "transfer_to": 29608,
        "transfer_status": "Completed",
        "created_at": "2001-05-11T08:37:33Z",
        "updated_at": "2001-05-12T09:37:33Z",
        "items": [
            {
                "item_id": "P003628",
                "amount": 18
            }
        ]
    }

    response = httpx.get(f"{BASE_URL}/transfers/800000", headers=headers)
    assert response.json() == None
    # first I get a non existing transfer
    response = httpx.post(f"{BASE_URL}/transfers",
                          headers=headers, json=new_transfer)
    assert response.status_code == 201
    # I check the response of adding a transfer
    response = httpx.get(f"{BASE_URL}/transfers/800000", headers=headers)
    assert response.json()["reference"] == "TR800000"
    # I check if it has actually been added
    response = httpx.delete(f"{BASE_URL}/transfers/800000", headers=headers)
    assert response.status_code == 200
    # I delete the updated warehouse
    response = httpx.get(f"{BASE_URL}/transfers/800000", headers=headers)
    assert response.json() == None
    # Once again I check if it's deleted


def test_delete_transfers():
    headers = {
        "api_key": "f6g7h8i9j0"
    }

    response = httpx.delete(f"{BASE_URL}/transfers/8000", headers=headers)
    assert response.status_code == 403
