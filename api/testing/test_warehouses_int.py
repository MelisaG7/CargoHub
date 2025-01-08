import httpx

# Replace with your actual API base URL
BASE_URL = "http://localhost:3000/api/v1"


def test_get_warehouses():
    headers = {
        "api_key": "a1b2c3d4e5"
    }
    response = httpx.get(f"{BASE_URL}/warehouses", headers=headers)
    assert response.status_code == 200


def test_get_one_warehouse():
    headers = {
        "api_key": "a1b2c3d4e5"
    }
    response = httpx.get(f"{BASE_URL}/warehouses/3", headers=headers)
    assert response.json()["code"] == "VCKINLLK"
    assert response.status_code == 200


def test_add_delete_warehouse():
    headers = {
        "api_key": "a1b2c3d4e5"
    }

    new_warehouse = {
        "id": 200,
        "code": "WORKS",
        "name": "Naaldwijk distribution hub",
        "address": "Izesteeg 807",
        "zip": "1636 KI",
        "city": "Naaldwijk",
        "province": "Utrecht",
        "country": "NL",
        "contact": {
            "name": "Frederique van Wallaert",
            "phone": "(009) 4870289",
            "email": "jelle66@example.net"
        },
        "created_at": "2001-05-11 10:43:52",
        "updated_at": "2017-12-19 14:32:38"
    }
    updated_warehouse = {
        "id": 200,
        "code": "UPDATED",
        "name": "Naaldwijk distribution hub",
        "address": "Izesteeg 807",
        "zip": "1636 KI",
        "city": "Naaldwijk",
        "province": "Utrecht",
        "country": "NL",
        "contact": {
            "name": "Frederique van Wallaert",
            "phone": "(009) 4870289",
            "email": "jelle66@example.net"
        },
        "created_at": "2001-05-11 10:43:52",
        "updated_at": "2017-12-19 14:32:38"
    }
    response = httpx.get(f"{BASE_URL}/warehouses/200", headers=headers)
    assert response.json() == None
    # first I get a non existing warehouse
    response = httpx.post(f"{BASE_URL}/warehouses",
                          headers=headers, json=new_warehouse)
    assert response.status_code == 201
    # I check the response of adding a warehouse
    response = httpx.get(f"{BASE_URL}/warehouses/200", headers=headers)
    assert response.json()["code"] == "WORKS"
    # I check if it has actually been added
    response = httpx.put(f"{BASE_URL}/warehouses/200",
                         headers=headers, json=updated_warehouse)
    response = httpx.get(f"{BASE_URL}/warehouses/200", headers=headers)
    assert response.json()["code"] == "UPDATED"
    # I check if it has actually been updated
    httpx.delete(f"{BASE_URL}/warehouses/200", headers=headers)
    # I delete the updated warehouse
    response = httpx.get(f"{BASE_URL}/warehouses/200", headers=headers)
    assert response.json() == None
    # Once again I check if it's deleted
