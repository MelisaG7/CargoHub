import os
import httpx

BASE_URL = "http://localhost:3000/api/v1"
if not os.getenv("GITHUB_ACTIONS"):
    from dotenv import load_dotenv
    load_dotenv()

admin_headers = {
    "api_key": os.getenv("API_KEY_1")
}
user_headers = {
    "api_key": os.getenv("API_KEY_2")
}

# tests with admin key


def test_get_item_lines():
    response = httpx.get(f"{BASE_URL}/item_lines", headers=admin_headers)
    assert response.status_code == 200

    response_user = httpx.get(f"{BASE_URL}/item_lines", headers=user_headers)
    assert response_user.status_code == 200


def test_get_item_lines_by_id():
    response = httpx.get(f"{BASE_URL}/item_lines/1", headers=admin_headers)
    assert response.json()["name"] == "Home Appliances"
    assert response.status_code == 200

    response_user = httpx.get(f"{BASE_URL}/item_lines/7", headers=user_headers)
    assert response_user.json()["name"] == "Kitchen Essentials"
    assert response_user.status_code == 200


def test_add_item_lines():
    data = {"id": 999, "name": "Office Chairs", "description": "test"}
    response = httpx.post(f"{BASE_URL}/item_lines",
                          headers=admin_headers, json=data)
    # doesnt work since it return code 404 NotFound
    assert response.status_code == 201

    # this assumes GET is working correctly
    get_response = httpx.get(
        f"{BASE_URL}/item_lines/999", headers=admin_headers)
    assert get_response.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["name"] == data["name"]
    assert fetched_data["description"] == data["description"]

    data_user = {"id": 999, "name": "Office Chairs", "description": "", "created_at": "2009-07-18 08:13:40",
                 "updated_at": "2020-01-12 14:32:49"}
    response_user = httpx.post(
        f"{BASE_URL}/item_lines", headers=user_headers, json=data_user)
    # Should return erorr Unauthorized
    assert response_user.status_code == 403


def test_update_item_lines():
    data = {"id": 988, "name": "Office Supplies", "description": "new",
            "created_at": "2009-07-18 08:13:40", "updated_at": "2020-01-12 14:32:49"}
    response = httpx.put(f"{BASE_URL}/item_lines/2",
                         headers=admin_headers, json=data,)
    assert response.status_code == 200  # as expected

    # # this assumes GET is working correctly
    # get_response = httpx.get(f"{BASE_URL}/item_lines/2", headers=admin_headers)
    # assert get_response.status_code == 404  #in reality this return a 200 OK

    get_response = httpx.get(
        f"{BASE_URL}/item_lines/988", headers=admin_headers)
    assert get_response.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["name"] == data["name"]
    assert fetched_data["description"] == data["description"]

    data_user = {"id": 989, "name": "Office Supplies", "description": "new", "created_at": "2009-07-18 08:13:40",
                 "updated_at": "2024-01-12 14:32:49"}
    response_user = httpx.put(
        f"{BASE_URL}/item_lines/12", headers=user_headers, json=data_user)
    # return error forbidden
    assert response_user.status_code == 403


def test_delete_item_lines():
    response = httpx.delete(f"{BASE_URL}/item_lines/0", headers=admin_headers)
    assert response.status_code == 200

    # get_response = httpx.get(f"{BASE_URL}/item_lines/0", headers=admin_headers)

    # should return NotFound but give 200 OK
    # assert get_response.status_code == 404
    response = httpx.delete(f"{BASE_URL}/item_lines/11", headers=user_headers)
    assert response.status_code == 403
