import pytest
from unittest.mock import MagicMock, patch
from models.orders import Orders
from providers import data_provider

@pytest.fixture
def orders():
    # Mock root_path en maak een Orders-instantie aan
    with patch("models.orders.ORDERS", []):
        return Orders(root_path="/path/to/", is_debug=True)

def test_get_orders(orders):
    orders.data = [{"id": 1}, {"id": 2}]
    assert orders.get_orders() == [{"id": 1}, {"id": 2}]

def test_get_order(orders):
    orders.data = [{"id": 1}, {"id": 2}]
    assert orders.get_order(1) == {"id": 1}
    assert orders.get_order(3) is None

def test_get_items_in_order(orders):
    orders.data = [{"id": 1, "items": ["item1", "item2"]}]
    assert orders.get_items_in_order(1) == ["item1", "item2"]
    assert orders.get_items_in_order(2) is None

def test_get_orders_in_shipment(orders):
    orders.data = [{"id": 1, "shipment_id": 10}, {"id": 2, "shipment_id": 20}]
    assert orders.get_orders_in_shipment(10) == [1]
    assert orders.get_orders_in_shipment(30) == []

def test_get_orders_for_client(orders):
    orders.data = [{"id": 1, "ship_to": 100, "bill_to": 200}, {"id": 2, "ship_to": 200, "bill_to": 200}]
    assert orders.get_orders_for_client(200) == [{"id": 1, "ship_to": 100, "bill_to": 200}, {"id": 2, "ship_to": 200, "bill_to": 200}]
    assert orders.get_orders_for_client(300) == []

def test_add_order(orders):
    orders.data = []
    with patch("models.base.Base.get_timestamp", return_value="2024-10-31"):
        orders.add_order({"id": 3, "items": []})
    assert orders.data[0]["created_at"] == "2024-10-31"
    assert orders.data[0]["updated_at"] == "2024-10-31"

def test_update_order(orders):
    orders.data = [{"id": 1, "items": []}]
    with patch("models.base.Base.get_timestamp", return_value="2024-10-31"):
        orders.update_order(1, {"id": 1, "items": ["item1"]})
    assert orders.data[0]["updated_at"] == "2024-10-31"
    assert orders.data[0]["items"] == ["item1"]

def test_update_items_in_order(orders):
    orders.data = [{"id": 1, "items": [{"item_id": "item1", "amount": 5}]}]
    items = [{"item_id": "item1", "amount": 10}]
    
    # Mock het data_provider-inventarispool
    mock_inventory_pool = MagicMock()
    mock_inventory_pool.get_inventories_for_item.return_value = [{"id": 1, "total_allocated": 100, "total_on_hand": 200}]
    with patch("providers.data_provider.fetch_inventory_pool", return_value=mock_inventory_pool):
        orders.update_items_in_order(1, items)
    
    # Controleren dat `update_inventory` wordt aangeroepen
    assert mock_inventory_pool.update_inventory.called

def test_update_orders_in_shipment(orders):
    orders.data = [{"id": 1, "shipment_id": 10, "order_status": "Scheduled"}, {"id": 2, "shipment_id": 20, "order_status": "Packed"}]
    orders.update_orders_in_shipment(10, [1])
    
    assert orders.get_order(1)["shipment_id"] == 10
    assert orders.get_order(1)["order_status"] == "Packed"
    assert orders.get_order(2)["shipment_id"] == 20

def test_remove_order(orders):
    orders.data = [{"id": 1}, {"id": 2}]
    orders.remove_order(1)
    assert orders.get_order(1) is None
    assert len(orders.data) == 1
