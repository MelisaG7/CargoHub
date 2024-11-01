import httpx
# from unittest.mock import *

BASE_URL = "http://localhost:3000/api/v1"
admin_headers = {
    "api_key": "a1b2c3d4e5"
}
user_headers = {
    "api_key": "f6g7h8i9j0"
}

# tests with admin key
def test_get_items_admin():
    response = httpx.get(f"{BASE_URL}/items", headers=admin_headers)
    assert response.status_code == 200

def test_get_item_by_id_admin():
    response = httpx.get(f"{BASE_URL}/items/P000001", headers=admin_headers)
    assert response.json()["uid"] == "P000001"
    assert response.status_code == 200

def test_get_items_for_item_line_admin():
    item_line_id = 58
    response = httpx.get(f"{BASE_URL}/items?item_line={item_line_id}", headers=admin_headers)
    assert response.status_code == 200
    # assert response.json()["item_line"] == 58

def test_get_items_for_item_group_admin():
    item_group_id = 50
    response = httpx.get(f"{BASE_URL}/items?item_group={item_group_id}", headers=admin_headers)
    assert response.status_code == 200

    # assert response.json()["item_group"] == 50

def test_get_items_for_item_type_admin():
    item_type_id = 63
    response = httpx.get(f"{BASE_URL}/items?item_type={item_type_id}", headers=admin_headers)
    assert response.status_code == 200 # returns error 404
    # items = response.json()
    # assert items[0]["item_type"] == 63
    # assert isinstance(items, list), "Expected a list of items in the response."

def test_get_items_for_supplier_admin():
    supplier_id = 69
    response = httpx.get(f"{BASE_URL}/items?supplier_id={supplier_id}", headers=admin_headers)
    assert response.status_code == 200 # retrun code 404 notfound
    # assert response.json()[0]["supplier_id"] == 69

def test_add_items_admin():
    data = {
        "uid": "P011722",
        "code": "sjQ23408K",
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "2015-02-19 16:08:24",
        "updated_at": "2015-09-26 06:37:56"
    }
    response = httpx.post(f"{BASE_URL}/items", headers=admin_headers, json=data,)
    assert response.status_code == 201

    # this assumes GET is working correctly
    get_response = httpx.get(f"{BASE_URL}/items/P011722", headers=admin_headers)
    # assert get_response.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["uid"] == data["uid"]
    assert fetched_data["description"] == data["description"]

def test_update_items_admin():
    data = {
        "uid": "P011723",
        "code": "sjQ23408K",
        "description": "test",
        "short_description": "must have",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "2015-02-19 16:08:24",
        "updated_at": "2015-09-26 06:37:56"
    } 
    response = httpx.put(f"{BASE_URL}/items/P000002", headers=admin_headers, json=data,)
    assert response.status_code == 200

    # # this assumes GET is working correctly
    # get_response = httpx.get(f"{BASE_URL}/items/P011722", headers=admin_headers)
    # assert get_response.status_code == 404  # Ensure the old data is not found anymore

    get_response_updated = httpx.get(f"{BASE_URL}/items/P011723", headers=admin_headers)
    assert get_response_updated.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response_updated.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["uid"] == data["uid"]
    assert fetched_data["description"] == data["description"]

def test_delete_item_admin():
    response = httpx.delete(f"{BASE_URL}/items/P000003", headers=admin_headers)
    assert response.status_code == 200

    # get_response = httpx.get(f"{BASE_URL}/items/P000002", headers=admin_headers)

    # # should return NotFound
    # assert get_response.status_code == 404


# tests with client key which should only allow GET
def test_get_items():
    response = httpx.get(f"{BASE_URL}/items", headers=user_headers)
    assert response.status_code == 200

def test_get_item_by_id():
    response = httpx.get(f"{BASE_URL}/items/P000001", headers=user_headers)
    assert response.json()["uid"] == "P000001"
    assert response.status_code == 200

def test_get_items_for_item_line():
    item_line_id = 11
    response = httpx.get(f"{BASE_URL}/items?item_line={item_line_id}", headers=admin_headers)
    assert response.json()["item_line"] == 11
    assert response.status_code == 200

def test_get_items_for_item_group():
    item_group_id = 73
    response = httpx.get(f"{BASE_URL}/items?item_group={item_group_id}", headers=admin_headers)
    assert response.json()["item_group"] == 73
    assert response.status_code == 200

def test_get_items_for_item_type():
    item_type_id = 14
    response = httpx.get(f"{BASE_URL}/items?item_type={item_type_id}", headers=admin_headers)
    assert response.json()["item_type"] == 14
    assert response.status_code == 200

def test_get_items_for_supplier():
    supplier_id = 34
    response = httpx.get(f"{BASE_URL}/items?supplier_id={supplier_id}", headers=admin_headers)
    assert response.json()["supplier_id"] == 34
    assert response.status_code == 200


def test_add_item_lines():
    data = {
        "uid": "P011723",
        "code": "sjQ23408K",
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "2015-02-19 16:08:24",
        "updated_at": "2015-09-26 06:37:56"
    } 
    response = httpx.post(f"{BASE_URL}/items", headers=user_headers, json=data,)
    # Should return erorr Unauthorized
    assert response.status_code == 403



def test_update_item_lines():
    data = {
        "uid": "P011723",
        "code": "sjQ23408K",
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "2015-02-19 16:08:24",
        "updated_at": "2015-09-26 06:37:56"
    } 
    response = httpx.put(f"{BASE_URL}/items/P011722", headers=user_headers, json=data,)
    # return error unauthorized since only the admin should be authorized
    assert response.status_code == 403


 
def test_delete_item_lines():
    response = httpx.delete(f"{BASE_URL}/items/P011723", headers=user_headers)
    assert response.status_code == 403

