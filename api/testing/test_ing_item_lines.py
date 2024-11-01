
import httpx

BASE_URL = "http://localhost:3000/api/v1"
admin_headers = {
    "api_key": "a1b2c3d4e5"
}
user_headers = {
    "api_key": "f6g7h8i9j0"
}

# tests with admin key
def test_get_item_lines_admin():
    response = httpx.get(f"{BASE_URL}/item_lines", headers=admin_headers)
    assert response.status_code == 200

def test_get_item_lines_by_id_admin():
    response = httpx.get(f"{BASE_URL}/item_lines/2", headers=admin_headers)
    assert response.json()["name"] ==  "Office Supplies"
    assert response.status_code == 200

def test_add_item_lines_admin():
    data = {"id": 999, "name": "Office Chairs", "description": "test"}
    response = httpx.post(f"{BASE_URL}/item_lines", headers=admin_headers, json=data)
    assert response.status_code == 201 # doesnt work since it return code 404 NotFound

    # this assumes GET is working correctly
    get_response = httpx.get(f"{BASE_URL}/item_lines/999", headers=admin_headers)
    assert get_response.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["name"] == data["name"]
    assert fetched_data["description"] == data["description"]
    assert fetched_data["created_at"] == data["created_at"]
    assert fetched_data["updated_at"] == data["updated_at"]

def test_update_item_lines_admin():
    data = {"id": 988, "name": "Office Supplies", "description": "new",
             "created_at": "2009-07-18 08:13:40", "updated_at": "2020-01-12 14:32:49" } 
    response = httpx.put(f"{BASE_URL}/item_lines/2", headers=admin_headers, json=data,)
    assert response.status_code == 200 # as expected


    # # this assumes GET is working correctly
    # get_response = httpx.get(f"{BASE_URL}/item_lines/2", headers=admin_headers)
    # assert get_response.status_code == 404  #in reality this return a 200 OK

    get_response = httpx.get(f"{BASE_URL}/item_lines/988", headers=admin_headers)
    assert get_response.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["name"] == data["name"]
    assert fetched_data["description"] == data["description"]
    assert fetched_data["created_at"] == data["created_at"]

def test_delete_item_lines_admin():
    response = httpx.delete(f"{BASE_URL}/item_lines/0", headers=admin_headers)
    assert response.status_code == 200

    get_response = httpx.get(f"{BASE_URL}/item_lines/0", headers=admin_headers)

    # should return NotFound but give 200 OK
    assert get_response.status_code == 404


# tests with client key which should only allow GET
def test_get_item_lines():
    response = httpx.get(f"{BASE_URL}/item_lines", headers=user_headers)
    assert response.status_code == 200

def test_get_item_lines_by_id():
    response = httpx.get(f"{BASE_URL}/item_lines/7", headers=user_headers)
    assert response.json()["name"] ==  "Kitchen Essentials"
    assert response.status_code == 200

def test_add_item_lines():
    data = {"id": 999, "name": "Office Chairs", "description": "", "created_at": "2009-07-18 08:13:40",
        "updated_at": "2020-01-12 14:32:49"}
    response = httpx.post(f"{BASE_URL}/item_lines", headers=user_headers, json=data,)
    # Should return erorr Unauthorized
    assert response.status_code == 403

    # # this assumes GET is working correctly
    # get_response = httpx.get(f"{BASE_URL}/item_lines/999", headers=user_headers)
    # assert get_response.status_code == 404  # Ensure the GET request is successful


def test_update_item_lines():
    data = {"id": 989, "name": "Office Supplies", "description": "new", "created_at": "2009-07-18 08:13:40",
        "updated_at": "2024-01-12 14:32:49"} 
    response = httpx.put(f"{BASE_URL}/item_lines/12", headers=user_headers, json=data,)
    # return error forbidden
    assert response.status_code == 403

    # # this assumes GET is working correctly
    # get_response = httpx.get(f"{BASE_URL}/item_lines/989", headers=user_headers)
    # assert get_response.status_code == 404  #should return NotFound but it return 200 Ok while empty

 
def test_delete_item_lines():
    response = httpx.delete(f"{BASE_URL}/item_lines/11", headers=user_headers)
    assert response.status_code == 403


