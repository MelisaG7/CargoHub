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
def test_get_items():
    response = httpx.get(f"{BASE_URL}/items", headers=admin_headers)
    assert response.status_code == 200

    response_user = httpx.get(f"{BASE_URL}/items", headers=user_headers)
    assert response_user.status_code == 200

def test_get_item_by_id_admin():
    response = httpx.get(f"{BASE_URL}/items/P000001", headers=admin_headers)
    assert response.json()["uid"] == "P000001"
    assert response.status_code == 200

    response_user = httpx.get(f"{BASE_URL}/items/P000001", headers=user_headers)
    assert response_user.json()["uid"] == "P000001"
    assert response_user.status_code == 200

def test_get_items_for_item_line():
    item_line_id = 58
    response = httpx.get(f"{BASE_URL}/items?item_line={item_line_id}", headers=admin_headers)
    assert response.status_code == 200
    
    item_line_id_user = 11
    response_user = httpx.get(f"{BASE_URL}/items?item_line={item_line_id_user}", headers=user_headers)
    assert response_user.json()["item_line"] == 11
    assert response_user.status_code == 200

def test_get_items_for_item_group():
    item_group_id = 50
    response = httpx.get(f"{BASE_URL}/items?item_group={item_group_id}", headers=admin_headers)
    assert response.status_code == 200

    item_group_id_user = 73
    response_user = httpx.get(f"{BASE_URL}/items?item_group={item_group_id_user}", headers=user_headers)
    assert response_user.json()["item_group"] == 73
    assert response_user.status_code == 200

def test_get_items_for_item_type():
    item_type_id = 63
    response = httpx.get(f"{BASE_URL}/items?item_type={item_type_id}", headers=admin_headers)
    assert response.status_code == 200 # returns error 404
    
    item_type_id_user = 14
    response_user = httpx.get(f"{BASE_URL}/items?item_type={item_type_id_user}", headers=user_headers)
    assert response_user.json()["item_type"] == 14
    assert response_user.status_code == 200

def test_get_items_for_supplier():
    supplier_id = 69
    response = httpx.get(f"{BASE_URL}/items?supplier_id={supplier_id}", headers=admin_headers)
    assert response.status_code == 200 # retrun code 404 notfound
    
    supplier_id = 34
    response = httpx.get(f"{BASE_URL}/items?supplier_id={supplier_id}", headers=user_headers)
    assert response.json()["supplier_id"] == 34
    assert response.status_code == 200

def test_add_items():
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

    data_user = {
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
    response_user = httpx.post(f"{BASE_URL}/items", headers=user_headers, json=data_user)
    # Should return erorr Unauthorized
    assert response_user.status_code == 403

def test_update_items():
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

    get_response_updated = httpx.get(f"{BASE_URL}/items/P011723", headers=admin_headers)
    assert get_response_updated.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response_updated.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["uid"] == data["uid"]
    assert fetched_data["description"] == data["description"]

    data_user = {
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
    response_user = httpx.put(f"{BASE_URL}/items/P011722", headers=user_headers, json=data_user)
    # return error unauthorized since only the admin should be authorized
    assert response_user.status_code == 403

def test_delete_item():
    response = httpx.delete(f"{BASE_URL}/items/P000003", headers=admin_headers)
    assert response.status_code == 200

    response_user = httpx.delete(f"{BASE_URL}/items/P011723", headers=user_headers)
    assert response_user.status_code == 403


  


 

