import pytest
import httpx
import json

BASE_URL = "http://localhost:3000/api/v1/item_groups"


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
        self.original_data = self.load_all_item_group_data()

        yield

        self.teardown()

    def load_all_item_group_data(self):
        with open('data/item_groups.json', 'r') as file:
            return json.load(file)

    def restore_original_data(self):
        with open('data/item_groups.json', 'w') as file:
            json.dump(self.original_data, file)

    def load_item_group_data(self, item_group_id):
        try:
            with open('data/item_groups.json', 'r') as file:
                data = json.load(file)
                
                if not isinstance(data, list):
                    print("Error: JSON data is not a list.")
                    return None
                
                for item_group in data:
                    # Ensure each item is a dictionary
                    if isinstance(item_group, dict):
                        # Print debug information for each id comparison
                        print(f"Checking item_group with id: {item_group.get('id')} (type: {type(item_group.get('id'))})")
                        print(f"Against provided item_group_id: {item_group_id} (type: {type(item_group_id)})")

                        if item_group.get("id") == item_group_id:
                            print("Match found.")
                            return item_group
                    else:
                        print("Warning: Non-dictionary item found in data list.")
                
                # If we exit the loop, no match was found
                print("No matching id found.")
                return None

        except FileNotFoundError:
            print("Error: 'data/item_groups.json' file not found.")
            return None
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON data.")
            return None


    def teardown(self):
        self.restore_original_data()

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
            assert response.status_code == 500
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
        assert response.status_code == 500
        # Dit geeft mij weer 404 maar waarom MANNNNN!
        # Kan dat uberhaupt bij post?!

    def test_put_item_group(self):
        response = httpx.put(f"{BASE_URL}/{1}", json=self.DummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 200
        updated_item_group_data = self.load_item_group_data(self.DummyItem_group["id"])
        assert updated_item_group_data["name"] == self.DummyItem_group["name"]

        response = httpx.put(f"{BASE_URL}/{1}", json=self.DummyItem_group, headers=self.headerlist[1])
        assert response.status_code == 403
        # Klopt

        response = httpx.put(f"{BASE_URL}/{1}", json=self.WrongDummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 500
        # Klopt niet

    def test_remove_item_group(self):
        # response = httpx.post(f"{BASE_URL}", json=self.DummyItem_group, headers=self.headerlist[0])
        response = httpx.delete(f"{BASE_URL}/{31}", headers=self.headerlist[0])
        assert response.status_code == 200
        # 500 once again

        response = httpx.get(f"{BASE_URL}/{31}", headers=self.headerlist[0])
        assert response.status_code == 404
        # 500..


if __name__ == '__main__':
    pytest.main()
