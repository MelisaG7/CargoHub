import json
from services.base import Base
from fastapi import APIRouter, HTTPException, Body
from models.Models import Order, ItemFields
from fastapi.responses import JSONResponse
from typing import List

ORDERS = []


class Orders(Base):
    def __init__(self, root_path, is_debug=False):
        """Initialiseert de Orders-klasse met een pad naar het data-bestand.

        Args:
            root_path (str): Het basispad waar het JSON-data-bestand zich bevindt.
            is_debug (bool): Bepaalt of de klasse met debugdata moet worden geladen.
        """
        self.data_path = root_path + "orders.json"
        self.load(is_debug)
        self.router = APIRouter()

        # Check
        self.router.add_api_route("/orders/", self.get_orders, methods=["GET"])
        # Check
        self.router.add_api_route(
            "/orders/{order_id}", self.get_order, methods=["GET"])
        # Check (moet nog nacontrole doen)
        self.router.add_api_route(
            "/orders/{order_id}/items", self.get_items_in_order, methods=["GET"])
        # Moet nog nacontrole doen
        self.router.add_api_route(
            "/shipments/{shipment_id}/orders", self.get_orders_in_shipment, methods=["GET"])
        # Moet nog nacontrole doen
        self.router.add_api_route(
            "/clients/{client_id}/orders", self.get_orders_for_client, methods=["GET"])
        # Moet nog nacontrole doen
        self.router.add_api_route("/orders/", self.add_order, methods=["POST"])
        self.router.add_api_route(
            "/orders/{order_id}", self.update_order, methods=["PUT"])
        # Moet nog nacontrole doen
        self.router.add_api_route(
            "/orders/{order_id}/items", self.update_items_in_order, methods=["PUT"])
        # Moet nog nacontrole doen
        self.router.add_api_route(
            "/shipments/{shipment_id}/orders", self.update_orders_in_shipment, methods=["PUT"])
        self.router.add_api_route(
            "/orders/{order_id}", self.remove_order, methods=["DELETE"])

    @staticmethod
    def Fouthandling():
        from Fouthandling.orders_fouthandling import OrderFouthandling
        return OrderFouthandling()

    def DataProvider():
        from providers import data_provider
        return data_provider

    def get_orders(self):
        """Haalt alle bestellingen op uit de data.

        Returns:
            list: Een lijst met alle bestellingen.
        """
        return self.data

    def get_order(self, order_id: int):
        if not self.Fouthandling().check_get_order(order_id):
            raise HTTPException(status_code=400, detail="invalid order id")
        """Zoekt en retourneert een specifieke bestelling op basis van het order-ID.

        Args:
            order_id (int): Het ID van de bestelling om op te halen.

        Returns:
            dict or None: De bestelgegevens als een dictionary als deze bestaat, anders None.
        """
        for order in self.data:
            if order["id"] == order_id:
                return order
        raise HTTPException(status_code=400, detail="invalid order id")

    def get_items_in_order(self, order_id: int):
        if not self.Fouthandling().check_get_order(order_id):
            raise HTTPException(status_code=400, detail="invalid order id")
        """Haalt alle items op binnen een specifieke bestelling.

        Args:
            order_id (int): Het ID van de bestelling.

        Returns:
            list or None: Een lijst met items binnen de bestelling of None als de bestelling niet bestaat.
        """
        for order in self.data:
            if order["id"] == order_id:
                return order["items"]
        raise HTTPException(status_code=400, detail="Invalid order id.")

    def get_orders_in_shipment(self, shipment_id):
        if not self.Fouthandling().check_get_orders_in_shipment(shipment_id):
            raise HTTPException(status_code=400, detail="Invalid shipmemnt id.")
        """Haalt alle orders op die aan een specifieke zending zijn gekoppeld.

        Args:
            shipment_id (int): Het ID van de zending.

        Returns:
            list: Een lijst met order-ID's die aan de zending zijn gekoppeld.
        """
        result = []
        for order in self.data:
            if str(order["shipment_id"]) == shipment_id:
                result.append(order["id"])
        return result

    def get_orders_for_client(self, client_id):
        if not self.Fouthandling().check_get_orders_for_client(client_id):
            raise HTTPException(status_code=400, detail="Invalid client id")
        """Haalt alle bestellingen op voor een specifieke klant.

        Args:
            client_id (int): Het ID van de klant.

        Returns:
            list: Een lijst met bestellingen voor de klant.
        """
        result = []
        for order in self.data:
            if str(order["ship_to"]) == client_id or str(order["bill_to"]) == client_id:
                result.append(order)
        return result

    def add_order(self, order: Order):
        if not self.Fouthandling().check_add_order(order):
            raise HTTPException(status_code=400, detail="Invalid order body")
        """Voegt een nieuwe bestelling toe aan de data met tijdstempels voor aanmaak en update.

        Args:
            order (dict): De gegevens van de bestelling om toe te voegen.
        """
        order_dictionary = order.model_dump()
        order_dictionary["created_at"] = self.get_timestamp()
        order_dictionary["updated_at"] = self.get_timestamp()
        self.data.append(order_dictionary)
        self.save()
        return JSONResponse(content="order successfully added", status_code=201)

    def update_order(self, order_id: int, order: Order):
        if not self.Fouthandling().check_update_order(order_id, order):
            raise HTTPException(status_code=400, detail="Incorrect order id or order body.")
        """Werk een bestaande bestelling bij op basis van het order-ID.

        Args:
            order_id (int): Het ID van de bestelling om bij te werken.
            order (dict): De bijgewerkte bestelgegevens.
        """
        order_dictionary = order.model_dump()
        order_dictionary["updated_at"] = self.get_timestamp()
        for index in range(len(self.data)):
            if self.data[index]["id"] == order_id:
                self.data[index] = order_dictionary
                self.save()
                return JSONResponse(content="order is successfully updated", status_code=201)
        raise HTTPException(status_code=404, detail="order not found")

    def update_items_in_order(self, order_id, items: List[ItemFields] = Body(...)):
        if not self.Fouthandling().check_update_items_in_order(order_id, items):
            raise HTTPException(status_code=400, detail="Invalid order id or item list")
        """Werk de items binnen een bestelling bij en beheer de inventaris.

        Args:
            order_id (int): Het ID van de bestelling om bij te werken.
            items (list): De bijgewerkte lijst met items binnen de bestelling.
        """
        order = self.get_order(order_id)
        current_items = order["items"]

        # Verwijder items die niet meer in de bestelling zijn
        for current_item in current_items:
            found = False
            for new_item in items:
                if current_item["item_id"] == new_item["item_id"]:
                    found = True
                    break
            if not found:
                inventories = self.DataProvider().fetch_inventory_pool(
                ).get_inventories_for_item(current_item["item_id"])
                min_ordered = 1_000_000_000_000_000_000
                min_inventory = None
                for inventory in inventories:
                    if inventory["total_allocated"] > min_ordered:
                        min_ordered = inventory["total_allocated"]
                        min_inventory = inventory
                min_inventory["total_allocated"] -= current_item["amount"]
                min_inventory["total_expected"] = new_item["total_on_hand"] + \
                    new_item["total_ordered"]
                self.DataProvider().fetch_inventory_pool().update_inventory(
                    min_inventory["id"], min_inventory)

        # Voeg of update items die in de bestelling zijn
        for current_item in current_items:
            for new_item in items:
                if current_item["item_id"] == new_item["item_id"]:
                    inventories = self.DataProvider().fetch_inventory_pool(
                    ).get_inventories_for_item(current_item["item_id"])
                    min_ordered = 1_000_000_000_000_000_000
                    min_inventory
                    for inventory in inventories:
                        if inventory["total_allocated"] < min_ordered:
                            min_ordered = inventory["total_allocated"]
                            min_inventory = inventory
                min_inventory["total_allocated"] += new_item["amount"] - \
                    current_item["amount"]
                min_inventory["total_expected"] = new_item["total_on_hand"] + \
                    new_item["total_ordered"]
                self.DataProvider().fetch_inventory_pool().update_inventory(
                    min_inventory["id"], min_inventory)

        order["items"] = items
        self.update_order(order_id, order)

    def update_orders_in_shipment(self, shipment_id, orders):
        if not self.Fouthandling().check_update_orders_in_shipment(shipment_id, orders):
            raise HTTPException(status_code=400, detail="invalid shipment id or order list")
        """Werk de zending bij door orders toe te voegen of te verwijderen van een zending.

        Args:
            shipment_id (int): Het ID van de zending.
            orders (list): Een lijst met order-ID's die bij de zending horen.
        """
        # Get all current packed orders
        current_orders = set(self.get_orders_in_shipment(shipment_id))
        new_orders = set(json.loads(orders))

        # Orders to remove
        for packed_order_id in current_orders - new_orders:
            order = self.get_order(packed_order_id)
            order["shipment_id"] = -1
            order["order_status"] = "Scheduled"
            self.update_order(packed_order_id, order)

        # Orders to add/update
        for packed_order_id in new_orders:
            order = self.get_order(packed_order_id)
            order["shipment_id"] = shipment_id
            order["order_status"] = "Packed"
            self.update_order(packed_order_id, order)

    def remove_order(self, order_id):
        if not self.Fouthandling().check_remove_order(order_id):
            raise HTTPException(status_code=400, detail="Invalid order id.")
        """Verwijdert een bestelling uit de data op basis van het order-ID.

        Args:
            order_id (int): Het ID van de bestelling om te verwijderen.
        """
        for order in self.data:
            if order["id"] == order_id:
                self.data.remove(order)
                self.save()
                return JSONResponse(content="Order successfully removed.", status_code=200)
        raise HTTPException(status_code=400, detail="Order not found")

    def load(self, is_debug):
        """Laadt de bestellingsgegevens uit een JSON-bestand of uit een debuglijst.

        Args:
            is_debug (bool): Bepaalt of debuggegevens moeten worden gebruikt.
        """
        if is_debug:
            self.data = ORDERS
        else:
            f = open(self.data_path, "r")
            self.data = json.load(f)
            f.close()

    def save(self):
        # """Saves the current data to the JSON file."""
        f = open(self.data_path, "w")
        json.dump(self.data, f)
