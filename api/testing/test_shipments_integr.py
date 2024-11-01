import pytest
import json
from models.shipments import Shipments  # Zorg ervoor dat je het juiste pad gebruikt voor je import

class TestShipments:

    @pytest.fixture(autouse=True)
    def setup(self):
        # Stel de root_path en testdata in
        self.root_path = "./"  # Pas dit aan naar het pad waar je testdata wilt opslaan
        self.shipments_data = [
            {
                "id": 1,
                "items": [{"item_id": "A001", "amount": 10}],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "items": [{"item_id": "B002", "amount": 5}],
                "created_at": "2024-01-02T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z"
            }
        ]

        # Maak een tijdelijke JSON-bestand voor de tests
        with open(self.root_path + "shipments.json", "w") as f:
            json.dump(self.shipments_data, f)

        # Initialiseer de Shipments klasse
        self.shipments = Shipments(self.root_path, is_debug=True)

    def test_get_shipments(self):
        all_shipments = self.shipments.get_shipments()
        assert len(all_shipments) == 2  # Verwacht dat er 2 zendingen zijn

    def test_get_shipment(self):
        shipment = self.shipments.get_shipment(1)
        assert shipment is not None
        assert shipment["id"] == 1

        shipment = self.shipments.get_shipment(3)  # Niet bestaande zending
        assert shipment is None

    def test_add_shipment(self):
        new_shipment = {
            "id": 3,
            "items": [{"item_id": "C003", "amount": 20}]
        }
        self.shipments.add_shipment(new_shipment)
        all_shipments = self.shipments.get_shipments()
        assert len(all_shipments) == 3  # We verwachten nu 3 zendingen

    def test_update_shipment(self):
        updated_shipment = {
            "id": 1,
            "items": [{"item_id": "A001", "amount": 15}],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
        self.shipments.update_shipment(1, updated_shipment)
        shipment = self.shipments.get_shipment(1)
        assert shipment["items"][0]["amount"] == 15

    def test_remove_shipment(self):
        self.shipments.remove_shipment(2)
        all_shipments = self.shipments.get_shipments()
        assert len(all_shipments) == 1  # Na verwijderen van zending 2 verwachten we 1 zending

    def teardown_method(self):
        # Ruim op: verwijder het tijdelijke bestand
        import os
        if os.path.exists(self.root_path + "shipments.json"):
            os.remove(self.root_path + "shipments.json")

if __name__ == '__main__':
    pytest.main()
