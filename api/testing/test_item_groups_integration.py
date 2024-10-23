import pytest
import httpx

BASE_URL = "http://localhost:3000/api/v1/item_groups"  # Vervang dit door de URL van je eigen server


class TestEndpointsItemGroups:

    @pytest.fixture(autouse=True)
    def setup(self):
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
            "id": 250,
            "name": "Shoes",
            "description": ""
            }
        self.WrongDummyItem_group = {
            "name": "Designer Heels"
        }

    def test_get_item_groups(self):
        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[1])
        assert response.status_code == 200

    def test_get_item_group(self):
        response = httpx.get(f"{BASE_URL}/{1}", headers=self.headerlist[0])
        assert response.status_code == 200
        assert response.json()["id"] == 1

        response = httpx.get(f"{BASE_URL}/{1}", headers=self.headerlist[1])
        assert response.status_code == 200

        for Id in self.WrongIds:
            response = httpx.get(f"{BASE_URL}/{Id}", headers=self.headerlist[0])
            assert response.status_code == 500
            # Hier werken min getallen well. De resultaat is dan null ipv een item_group object

    def test_post_item_group(self):
        response = httpx.post(f"{BASE_URL}", json=self.DummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 201

        response = httpx.post(f"{BASE_URL}", json=self.DummyItem_group, headers=self.headerlist[1])
        assert response.status_code == 403
        # Want normale user heeft beperkte rechten

        response = httpx.post(f"{BASE_URL}", json=self.WrongDummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 500 # of 400 idk
        # dit is ook fout want foute bodies worden er gewoon ingezet, geen fouthandling dus

    def test_put_item_group(self):
        response = httpx.put(f"{BASE_URL}/{1}", json=self.DummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{250}", headers=self.headerlist[0])
        assert response.json()["name"] == self.DummyItem_group["name"]

        response = httpx.put(f"{BASE_URL}/{1}", json=self.DummyItem_group, headers=self.headerlist[1])
        assert response.status_code == 403
        # user heeft beperkte rechten
        # Nu zou ik in de database moeten kijken of object met id 1 idd veranderd is naar dummy object.
        # Note: Eigelijk hoort de id niet te veranderen, maar gebeurd wel doordat de dummy id de nieuwe id wordt.
        # Hierdoor als je object met id nr 1 zoekt, krijg je null, wat niet hoort
        # Als ik een foute body stuur dan hoort het niet te werken idc

        response = httpx.put(f"{BASE_URL}/{1}", json=self.WrongDummyItem_group, headers=self.headerlist[0])
        assert response.status_code == 500
        # prolly werkt het wel, wat niet hoort

    def test_remove_item_group(self):
        httpx.post(f"{BASE_URL}", json=self.DummyItem_group, headers=self.headerlist[0])
        response = httpx.delete(f"{BASE_URL}/{250}", headers=self.headerlist[0])
        assert response.status_code == 200

        response = httpx.get(f"{BASE_URL}/{self.DummyItem_group["id"]}", headers=self.headerlist[0])
        assert response.status_code == 404
        # Nou in database checken of er echtwaar geen object met id 250 in zit


if __name__ == '__main__':
    pytest.main()
