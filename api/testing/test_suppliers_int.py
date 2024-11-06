import httpx

# Replace with your actual API base URL
BASE_URL = "http://localhost:3000/api/v1"


def test_get_suppliers():
    headers = {
        "api_key": "a1b2c3d4e5"
    }
    response = httpx.get(f"{BASE_URL}/suppliers", headers=headers)
    assert response.status_code == 200


def test_get_one_suppliers():
    headers = {
        "api_key": "a1b2c3d4e5"
    }
    response = httpx.get(f"{BASE_URL}/suppliers/41", headers=headers)
    assert response.json()["code"] == "SUP0041"
    assert response.status_code == 200


def test_add_delete_suppliers():
    headers = {
        "api_key": "a1b2c3d4e5"
    }
    new_suppliers = {
        "id": 910,
        "code": "SUP0041",
        "name": "NEW SUPPLY Inc",
        "address": "2219 Steven Mountains Suite 602",
        "address_extra": "Suite 283",
        "city": "West Tiffanyhaven",
        "zip_code": "22233",
        "province": "Iowa",
        "country": "Turkey",
        "contact_name": "Sarah Lloyd",
        "phonenumber": "612-651-8439",
        "reference": "BI-SUP0041",
        "created_at": "1970-05-05 04:12:12",
        "updated_at": "1998-08-03 13:52:24"
    }
    updated_suppliers = {
        "id": 910,
        "code": "SUP0041",
        "name": "UPDATED SUPPLY Inc",
        "address": "2219 Steven Mountains Suite 602",
        "address_extra": "Suite 283",
        "city": "West Tiffanyhaven",
        "zip_code": "22233",
        "province": "Iowa",
        "country": "Turkey",
        "contact_name": "Sarah Lloyd",
        "phonenumber": "612-651-8439",
        "reference": "BI-SUP0041",
        "created_at": "1970-05-05 04:12:12",
        "updated_at": "1998-08-03 13:52:24"
    }
    response = httpx.get(f"{BASE_URL}/suppliers/910", headers=headers)
    assert response.json() == None
    # first I get a non existing suppliers
    response = httpx.post(f"{BASE_URL}/suppliers",
                          headers=headers, json=new_suppliers)
    assert response.status_code == 201
    # I check the response of adding a suppliers
    response = httpx.get(f"{BASE_URL}/suppliers/910", headers=headers)
    assert response.json()["name"] == "NEW SUPPLY Inc"
    # I check if it has actually been added
    response = httpx.put(f"{BASE_URL}/suppliers/910",
                         headers=headers, json=updated_suppliers)
    response = httpx.get(f"{BASE_URL}/suppliers/910", headers=headers)
    assert response.json()["name"] == "UPDATED SUPPLY Inc"
    # I check if it has actually been updated
    httpx.delete(f"{BASE_URL}/suppliers/910", headers=headers)
    # I delete the updated suppliers
    response = httpx.get(f"{BASE_URL}/suppliers/910", headers=headers)
    assert response.json() == None
    # Once again I check if it's deleted
