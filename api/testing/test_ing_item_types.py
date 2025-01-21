import httpx
import os

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


def test_get_item_types():
    response = httpx.get(f"{BASE_URL}/item_types", headers=admin_headers)
    assert response.status_code == 200

    response_user = httpx.get(f"{BASE_URL}/item_types", headers=user_headers)
    assert response_user.status_code == 200


def test_get_item_types_by_id():
    response = httpx.get(f"{BASE_URL}/item_types/2", headers=admin_headers)
    assert response.json()["name"] == "Tablet"
    assert response.status_code == 200

    response_user = httpx.get(f"{BASE_URL}/item_types/2", headers=user_headers)
    assert response_user.json()["name"] == "Tablet"
    assert response_user.status_code == 200


def test_add_item_types():
    data = {"id": 101, "name": "testAdds", "description": "testtype",
            "created_at": "2023-07-28 13:43:32", "updated_at": "2024-05-12 08:54:35"}
    response = httpx.post(f"{BASE_URL}/item_types",
                          headers=admin_headers, json=data)
    assert response.status_code == 201  # causes code 404 notfound

    get_response = httpx.get(
        f"{BASE_URL}/item_types/101", headers=admin_headers)
    # assert get_response.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["name"] == data["name"]
    assert fetched_data["description"] == data["description"]

    data_user = {"id": 999, "name": "Office Chairs", "description": "", "created_at": "2009-07-18 08:13:40",
                 "updated_at": "2020-01-12 14:32:49"}
    response_user = httpx.post(
        f"{BASE_URL}/item_types", headers=user_headers, json=data_user)
    # Should return erorr forbidden
    assert response_user.status_code == 403


def test_update_item_types():
    data = {"id": 105, "name": "testAdds", "description": "", "created_at": "2023-07-28 13:43:32",
            "updated_at": "2024-05-12 08:54:35"}

    response = httpx.put(f"{BASE_URL}/item_types/0",
                         headers=admin_headers, json=data,)
    assert response.status_code == 200

    # this assumes GET is working correctly
    get_response = httpx.get(
        f"{BASE_URL}/item_types/105", headers=admin_headers)
    assert get_response.status_code == 200  # Ensure the GET request is successful
    fetched_data = get_response.json()

    # Verify that the fetched data matches what was added
    assert fetched_data["name"] == data["name"]
    assert fetched_data["description"] == data["description"]

    data_user = {"id": 989, "name": "Office Supplies", "description": "new", "created_at": "2009-07-18 08:13:40",
                 "updated_at": "2024-01-12 14:32:49"}
    response_user = httpx.post(
        f"{BASE_URL}/item_types/3", headers=user_headers, json=data_user)
    # return error forbidden
    assert response_user.status_code == 403


def test_delete_item_types():
    response = httpx.delete(f"{BASE_URL}/item_types/6", headers=admin_headers)
    assert response.status_code == 200

    response_user = httpx.delete(
        f"{BASE_URL}/item_types/999", headers=user_headers)
    assert response_user.status_code == 403
