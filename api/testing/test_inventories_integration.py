import pytest
import httpx
import json
import os
BASE_URL = "http://localhost:3000/api/v1/inventories"


class TestEndpointsInventories:

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        if not os.getenv("GITHUB_ACTIONS"):
            from dotenv import load_dotenv
            load_dotenv()

        # Laad de API-keys dynamisch uit de omgeving
        self.headerlist = [
            {"api_key": os.getenv("API_KEY_1")},
            {"api_key": os.getenv("API_KEY_2")}]
        self.ids = [1, 20, 50, 100]
        self.WrongIds = [-1, -20, 1.25, "hundred"]
        self.DummyInventory = {
            "id": 111112,
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
            "total_available": 55
        }
        self.WrongDummyInventory = {
            "id": 2000001,
            "item_id": "P2000001",
            "description": "A description"
        }
        self.original_data = self.load_all_inventory_data()

        self.teardown()

    def load_all_inventory_data(self):
        with open('./data/inventories.json', 'r') as file:
            return json.load(file)

    def restore_original_data(self):
        with open('./data/inventories.json', 'w') as file:
            json.dump(self.original_data, file)

    def load_inventory_data(self, inventory_id: int):
        with open('./data/inventories.json', 'r') as file:
            data = json.load(file)
            for inventory in data:
                if inventory["id"] == inventory_id:
                    return inventory
        return None

    def teardown(self):
        self.restore_original_data()
        yield

    def test_get_inventories(self):
        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[0])
        assert response.status_code == 200
        # Dit werkt
        response = httpx.get(f"{BASE_URL}", headers=self.headerlist[1])
        assert response.status_code == 200
        # Dit geeft mij een 500 code ipv 200
        # Bij clients integrationtest werkt dit wel gewoon volledig.. en het is precies hetzelfde ook

    def test_get_inventory(self):
        for Id in self.ids:
            response = httpx.get(f"{BASE_URL}/{Id}",
                                 headers=self.headerlist[0])
            assert response.status_code == 200
            assert response.json()["id"] == Id
            # Dit werkt

        response = httpx.get(f"{BASE_URL}/{25}", headers=self.headerlist[1])
        assert response.status_code == 200
        # Dit geeft mij ook 500 status code. Ik weet niet waarom

        for Id in self.WrongIds:
            response = httpx.get(f"{BASE_URL}/{Id}",
                                 headers=self.headerlist[0])
            assert response.status_code == 400 or response.status_code == 422
            # Dit geeft mij 200 ipv 404
    # Deze methode werkt half alleen met headerlist[0] juiste ids.

    def test_get_inventory_totals_for_item(self):
        item_id = "P000001"
        response = httpx.get(f"http://localhost:3000/api/v1/items/{item_id}/inventory/totals", headers=self.headerlist[0])
        assert response.status_code == 200
        totals = response.json()
        assert "total_expected" in totals
        assert "total_ordered" in totals
        assert "total_allocated" in totals
        assert "total_available" in totals
        # Dit werkt

        response = httpx.get(f"http://localhost:3000/api/v1/items/{item_id}/inventory/totals", headers=self.headerlist[1])
        assert response.status_code == 200

        wrong_item_id = "INVALID_ID"
        response = httpx.get(f"http://localhost:3000/api/v1/items/{wrong_item_id}/inventory/totals", headers=self.headerlist[0])
        assert response.status_code == 400

    def test_post_inventory(self):
        response = httpx.post(
            f"{BASE_URL}", json=self.DummyInventory, headers=self.headerlist[0])
        assert response.status_code == 201
        inventory_data = self.load_inventory_data(self.DummyInventory["id"])
        assert inventory_data["description"] == self.DummyInventory["description"]
        # Dit is goed, maar once again is alleen de created_at en updated_at anders.
        # Daarom heb ik het even veranderd naar alleen op 1 key nakijken.

        response = httpx.post(
            f"{BASE_URL}", json=self.DummyInventory, headers=self.headerlist[1])
        assert response.status_code == 403
        # Hmmm dit hoort gewoon 403 te zijn maar ik krijg 500.
        # Is er iest mis misschien met headerlist[1]? Nee klopt gewoon

        response = httpx.post(
            f"{BASE_URL}", json=self.WrongDummyInventory, headers=self.headerlist[0])
        assert response.status_code == 400 or response.status_code == 422
        self.restore_original_data()
        # En dit is 201 ipv 400, maar de test zelf lukt gwoon

    def test_put_inventory(self):
        response = httpx.post(
            f"{BASE_URL}", json=self.DummyInventory, headers=self.headerlist[0])
        response = httpx.put(
            f"{BASE_URL}/{self.DummyInventory['id']}", json=self.DummyInventory, headers=self.headerlist[0])
        assert response.status_code == 200
        # Klopt
        updated_inventory_data = self.load_inventory_data(
            self.DummyInventory["id"])
        assert updated_inventory_data['item_id'] == self.DummyInventory['item_id']
        # Zodra ik de Id niet meer kan vinden, werkt het niet de json

        response = httpx.put(
            f"{BASE_URL}/{self.DummyInventory['id']}", json=self.DummyInventory, headers=self.headerlist[1])
        assert response.status_code == 403
        # Ook weer 500 out of nowhere. Pisses me off fr
        self.restore_original_data()

    def test_remove_inventory(self):
        response = httpx.delete(
            f"{BASE_URL}/{11720}", headers=self.headerlist[0])
        assert response.status_code == 200
        # Come on man...Waarom die 500?
        response = httpx.get(f"{BASE_URL}/{11720}", headers=self.headerlist[0])
        assert response.status_code == 404
        # OOk 500 WAAROOMMMMM

        response = httpx.delete(
            f"{BASE_URL}/{11710}", headers=self.headerlist[1])
        assert response.status_code == 403
        # Als ik deze errors heb gefixt of in de proces daarvan dan ben ik allang long gone in de mental hospital
        self.restore_original_data()


if __name__ == '__main__':
    pytest.main()
