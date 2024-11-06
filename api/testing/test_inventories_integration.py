import pytest
import httpx
import json

BASE_URL = "http://localhost:3000/api/v1/inventories"

class TestEndpointsInventories:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.headerlist = [
            {
                "api_key": "a1b2c3d4e5"
            },
            {
                "api_key": "f6g7h8i9j0"
            }
        ]
        self.ids = [1, 20, 50, 100]
        self.WrongIds = [-1, -20, 1.25, "hundred"]
        self.DummyInventory = {
            "id": 11721,
            "item_id": "P011721",
            "description": "2-weeks supplies to travel to Hermes",
            "item_reference": "nyg48736S",
            "locations": [
                19800,
                23653,
                3068,
                3334,
                20477,
                20524,
                17579,
                2271,
                2293,
                22717
            ],
            "total_on_hand": 194,
            "total_expected": 0,
            "total_ordered": 139,
            "total_allocated": 0,
            "total_available": 55,
            "created_at": "2020-05-31 16:00:08",
            "updated_at": "2020-11-08 12:49:21"
        }
        self.WrongDummyInventory = {
            "id": 2000001,
            "item_id": "P2000001",
            "description": "A description"
        }
        self.original_data = self.load_all_inventory_data()

        yield

        self.teardown()

    def load_all_inventory_data(self):
        with open('inventories.json', 'r') as file:
            return json.load(file)

    def restore_original_data(self):
        with open('inventories.json', 'w') as file:
            json.dump(self.original_data, file)

    def load_inventory_data(self, inventory_id):
        with open('inventories.json', 'r') as file:
            data = json.load(file)
            for inventory in data["inventories"]:
                if inventory["id"] == inventory_id:
                    return inventory
        return None

    def teardown(self):
        self.restore_original_data()

    def test_get_inventories(self):
        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[0])
        assert response.status_code == 200
        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[1])
        assert response.status_code == 403

    def test_get_inventory(self):
        for Id in self.ids:
            response = httpx.get(f"{BASE_URL}/{Id}", headers=self.headerlist[0])
            assert response.status_code == 200
            assert response.json()["id"] == Id
        
        for Id in self.WrongIds:
            response = httpx.get(f"{BASE_URL}/{Id}", headers=self.headerlist[0])
            assert response.status_code == 500
        
        response = httpx.get(f"{BASE_URL}/{25}", headers=self.headerlist[1])
        assert response.status_code == 403

    def test_post_inventory(self):
        response = httpx.post(f"{BASE_URL}", json=self.DummyInventory, headers=self.headerlist[0])
        assert response.status_code == 201
        inventory_data = self.load_inventory_data(self.DummyInventory["id"])
        assert inventory_data == self.DummyInventory

        response = httpx.post(f"{BASE_URL}", json=self.DummyInventory, headers=self.headerlist[1])
        assert response.status_code == 403

        response = httpx.post(f"{BASE_URL}/{11719}", json=self.WrongDummyInventory, headers=self.headerlist[0])
        assert response.status_code == 400

    def test_put_inventory(self):
        response = httpx.put(f"{BASE_URL}/{11720}", json=self.DummyInventory, headers=self.headerlist[0])
        assert response.status_code == 200
        updated_inventory_data = self.load_inventory_data(self.DummyInventory["id"])
        assert updated_inventory_data == self.DummyInventory

        response = httpx.put(f"{BASE_URL}/{11720}", json=self.DummyInventory, headers=self.headerlist[1])
        assert response.status_code == 403

    def test_remove_inventory(self):
        response = httpx.delete(f"{BASE_URL}/{11720}", headers=self.headerlist[0])
        assert response.status_code == 200
        response = httpx.get(f"{BASE_URL}/{11720}", headers=self.headerlist[0])
        assert response.status_code == 404

        response = httpx.delete(f"{BASE_URL}/{11710}", headers=self.headerlist[1])
        assert response.status_code == 403

if __name__ == '__main__':
    pytest.main()
