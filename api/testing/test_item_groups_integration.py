import pytest
import httpx
import json

BASE_URL = "http://localhost:3000/api/v1/itemgroups"


class TestEndpointsItemGroups:

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
        self.WrongIds = [-1, -20, "hundred"]
        self.DummyItem_group = {
            "id": 300,
            "name": "Shoes",
            "description": ""
        }
        self.WrongDummyItem_group = {
            "name": "Designer Heels"
        }
        self.original_data = self.load_all_item_groups_data()

        self.teardown()

    def load_all_item_groups_data(self):
        with open('./data/item_groups.json', 'r') as file:
            return json.load(file)

    def restore_original_data(self):
        with open('./data/item_groups.json', 'w') as file:
            json.dump(self.original_data, file)

    def load_item_group_data(self, inventory_id: int):
        with open('./data/item_groups.json', 'r') as file:
            data = json.load(file)
            for itemgroup in data:
                if itemgroup["id"] == inventory_id:
                    return itemgroup
        return None

    def teardown(self):
        self.restore_original_data()
        yield

    def test_get_item_groups(self):
        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[1])
        assert response.status_code == 200
        # Yayyyy werkt

    def test_get_item_group(self):
        response = httpx.get(f"{BASE_URL}/{1}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == 1

        response = httpx.get(f"{BASE_URL}/{1}", headers=self.headerlist[1])
        assert response.status_code == 200

        for Id in self.WrongIds:
            response = httpx.get(f"{BASE_URL}/{Id}", headers=self.headerlist[0])
            assert response.status_code == 400 or response.status_code == 422
            # Dit geet 200 terwijl dat niet hoort
        # Deze methode werkt ook volledig Yayyy

    def test_post_item_group(self):
        response = httpx.post(f"{BASE_URL}", json=self.DummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 201
        # # Heel raar, thunder geeft ook 404 ipv gewoon 201...?
        item_group_data = self.load_item_group_data(self.DummyItem_group["id"])
        assert item_group_data["description"] == self.DummyItem_group["description"]

        response = httpx.post(f"{BASE_URL}", json=self.DummyItem_group, headers=self.headerlist[1])
        assert response.status_code == 403
        # Dit werkt wel gewoon

        response = httpx.post(f"{BASE_URL}", json=self.WrongDummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 400 or response.status_code == 422
        # Dit geeft mij weer 404 maar waarom MANNNNN!
        # Kan dat uberhaupt bij post?!
        self.restore_original_data()

    def test_put_item_group(self):
        response = httpx.put(f"{BASE_URL}/{300}", json=self.DummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 201
        updated_item_group_data = self.load_item_group_data(self.DummyItem_group["id"])
        assert updated_item_group_data["name"] == self.DummyItem_group["name"]

        response = httpx.put(f"{BASE_URL}/{1}", json=self.DummyItem_group, headers=self.headerlist[1])
        assert response.status_code == 403
        # Klopt

        response = httpx.put(f"{BASE_URL}/{1}", json=self.WrongDummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 400 or response.status_code == 422
        # Klopt niet.
        self.restore_original_data()

    def test_remove_item_group(self):
        response = httpx.post(f"{BASE_URL}", json=self.DummyItem_group, headers=self.headerlist[0])
        response = httpx.delete(f"{BASE_URL}/{300}", headers=self.headerlist[0])
        assert response.status_code == 200
        # 500 once again

        response = httpx.get(f"{BASE_URL}/{300}", headers=self.headerlist[0])
        assert response.status_code == 404
        # 500..
        self.restore_original_data()


if __name__ == '__main__':
    pytest.main()