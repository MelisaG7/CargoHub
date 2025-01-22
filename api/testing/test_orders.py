import pytest
from services.orders import Orders
from fastapi import HTTPException


# Mock ORDERS data om mee te testen
ORDERS = [
    {"id": 1, "shipment_id": 101, "ship_to": "Client A", "bill_to": "Client A", "items": []},
    {"id": 2, "shipment_id": 102, "ship_to": "Client B", "bill_to": "Client B", "items": []},
    {"id": 3, "shipment_id": 103, "ship_to": "Client C", "bill_to": "Client C", "items": []},
]


def test_get_orders():
    orders = Orders(root_path="", is_debug=True)
    orders.data = ORDERS  # Mock data invoegen
    assert orders.get_orders() == ORDERS  # Controleer of we de juiste orders krijgen


def test_get_order():
    orders = Orders(root_path="", is_debug=True)
    orders.data = ORDERS
    assert orders.get_order(1) == ORDERS[0]  # Order 1 ophalen
    with pytest.raises(HTTPException):
        orders.get_order("Abrakadabra")
    with pytest.raises(HTTPException):
        orders.get_order(84298499)


def test_get_orders_in_shipment():
    orders = Orders(root_path="", is_debug=True)
    orders.data = ORDERS
    result = orders.get_orders_in_shipment('101')
    assert result == [1]  # Order 1 is de enige in shipment_id 101


def test_remove_order():
    orders = Orders(root_path="", is_debug=True)
    orders.data = ORDERS.copy()
    orders.remove_order(1)
    assert len(orders.data) == 2  # Controleer of de order is verwijderd
    assert all(x["id"] != 1 for x in orders.data)  # Controleer of geen order met id 1 meer bestaat
