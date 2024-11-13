import pytest
from models.shipments import Shipments

SHIPMENTS = [
    {"id": 1, "items": [{"item_id": 101, "amount": 5}], "shipment_status": "Pending"},
    {"id": 2, "items": [{"item_id": 102, "amount": 3}], "shipment_status": "Shipped"},
    {"id": 3, "items": [{"item_id": 101, "amount": 2}], "shipment_status": "Pending"},
]

# Testen voor de Shipments class
def test_get_shipments():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS  # Mock data invoegen
    assert ship.get_shipments() == SHIPMENTS  # Controleer of we de juiste zendingen krijgen

def test_get_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS
    assert ship.get_shipment(1) == SHIPMENTS[0]  # Zending 1 ophalen
    assert ship.get_shipment(999) is None  # Niet-bestaande zending moet None retourneren

def test_add_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    new_shipment = {"id": 4, "items": [{"item_id": 103, "amount": 1}], "shipment_status": "Pending"}
    ship.add_shipment(new_shipment)
    assert len(ship.data) == 4  # Controleer of de nieuwe zending is toegevoegd
    assert ship.data[-1]["id"] == 4  # De laatste zending moet de nieuwe zending zijn

def test_update_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    updated_shipment = {"id": 1, "items": [{"item_id": 101, "amount": 10}], "shipment_status": "Shipped"}
    ship.update_shipment(1, updated_shipment)
    assert ship.data[0]["items"][0]["amount"] == 10  # Zending moet zijn bijgewerkt

def test_remove_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    ship.remove_shipment(1)
    assert len(ship.data) == 2  # Controleer of de zending is verwijderd
    assert all(x["id"] != 1 for x in ship.data)  # Controleer of geen zending met id 1 meer bestaat

def test_get_items_in_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS
    assert ship.get_items_in_shipment(1) == SHIPMENTS[0]["items"]  # Items in zending 1 ophalen
    assert ship.get_items_in_shipment(999) is None  # Niet-bestaande zending moet None retourneren
