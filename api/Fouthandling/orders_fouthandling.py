from models.Models import Order
from typing import List
from models.Models import ItemFields
import json


class OrderFouthandling:

    def __init__(self):
        self.something = "something"

    @staticmethod
    def orders():
        from services.orders import Orders
        return Orders("./data/", False)

    @staticmethod
    def warehouses():
        from services.warehouses import Warehouses
        return Warehouses("./data/", False)

    @staticmethod
    def items():
        from services.items import Items
        return Items("./data/", False)

    @staticmethod
    def shipments():
        from services.shipments import Shipments
        return Shipments("./data/", False)

    def check_get_order(self, order_id):
        if isinstance(order_id, str) and not order_id.isdigit():
            return False
        # check op valid integer
        if (int(order_id) < 0):
            return False
        return True

    def check_get_orders_in_shipment(self, shipment_id):
        return self.check_get_order(shipment_id)

    def check_get_orders_for_client(self, client_id):
        return self.check_get_order(client_id)

    def check_add_order(self, order: Order):
        for bestelling in self.orders().data:
            if bestelling["id"] == order.model_dump()["id"]:
                return False
        # check warehouse id
        for magazijn in self.warehouses().data:
            if magazijn["id"] == order.warehouse_id:
                return True
        return False
        # check shipment id??

    def check_update_order(self, order_id, order: Order):
        if not self.check_get_order(order_id):
            return False
        if order_id != order.id:
            return False
        return True

    def check_update_items_in_order(self, order_id, items: List[ItemFields]):
        if not self.check_get_order(order_id):
            return False
        # check if items exist in database
        database_item_ids = {item2["uid"] for item2 in self.items().data}
        # Check if every item_id in items exists in the database
        for item in items:
            if not self.items().is_valid_uid(item.item_id):
                return False
            if item.item_id not in database_item_ids:
                return False
        # check if id exists in database
        for bestelling in self.orders().data:
            if bestelling["id"] == int(order_id):
                return True
        return False

    def check_update_orders_in_shipment(self, shipment_id, orders: list):
        print("Called!!!")
        if not self.check_get_order(shipment_id):
            return False
        print("Called2.0")
        converted_orders = json.loads(orders)
        for order in converted_orders:
            if not self.check_get_order(order):
                return False
        print("Called3.0")
        # check of shipment id bestaat in database
        shipment_ids = [shipment["id"] for shipment in self.shipments().data]
        if int(shipment_id) not in shipment_ids:
            return False
        # check of order ids bestaan in order database
        print("Called4.0")
        order_ids = [order["id"] for order in self.orders().data]
        for order in orders:
            if order not in order_ids:
                return False
        return True

    def check_remove_order(self, order_id):
        if not self.check_get_order(order_id):
            return False
        # check of order id een integer is
        # check of order id een valid integer is
        if int(order_id) < 0:
            return False
        return True
