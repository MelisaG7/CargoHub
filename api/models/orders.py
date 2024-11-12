import json

from models.base import Base
from providers import data_provider

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

    def get_orders(self):
        """Haalt alle bestellingen op uit de data.

        Returns:
            list: Een lijst met alle bestellingen.
        """
        return self.data

    def get_order(self, order_id):
        """Zoekt en retourneert een specifieke bestelling op basis van het order-ID.
        
        Args:
            order_id (int): Het ID van de bestelling om op te halen.
        
        Returns:
            dict or None: De bestelgegevens als een dictionary als deze bestaat, anders None.
        """
        for x in self.data:
            if x["id"] == order_id:
                return x
        return None

    def get_items_in_order(self, order_id):
        """Haalt alle items op binnen een specifieke bestelling.
        
        Args:
            order_id (int): Het ID van de bestelling.
        
        Returns:
            list or None: Een lijst met items binnen de bestelling of None als de bestelling niet bestaat.
        """
        for x in self.data:
            if x["id"] == order_id:
                return x["items"]
        return None

    def get_orders_in_shipment(self, shipment_id):
        """Haalt alle orders op die aan een specifieke zending zijn gekoppeld.
        
        Args:
            shipment_id (int): Het ID van de zending.
        
        Returns:
            list: Een lijst met order-ID's die aan de zending zijn gekoppeld.
        """
        result = []
        for x in self.data:
            if x["shipment_id"] == shipment_id:
                result.append(x["id"])
        return result

    def get_orders_for_client(self, client_id):
        """Haalt alle bestellingen op voor een specifieke klant.
        
        Args:
            client_id (int): Het ID van de klant.
        
        Returns:
            list: Een lijst met bestellingen voor de klant.
        """
        result = []
        for x in self.data:
            if x["ship_to"] == client_id or x["bill_to"] == client_id:
                result.append(x)
        return result

    def add_order(self, order):
        """Voegt een nieuwe bestelling toe aan de data met tijdstempels voor aanmaak en update.
        
        Args:
            order (dict): De gegevens van de bestelling om toe te voegen.
        """
        order["created_at"] = self.get_timestamp()
        order["updated_at"] = self.get_timestamp()
        self.data.append(order)

    def update_order(self, order_id, order):
        """Werk een bestaande bestelling bij op basis van het order-ID.
        
        Args:
            order_id (int): Het ID van de bestelling om bij te werken.
            order (dict): De bijgewerkte bestelgegevens.
        """
        order["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == order_id:
                self.data[i] = order
                break

    def update_items_in_order(self, order_id, items):
        """Werk de items binnen een bestelling bij en beheer de inventaris.
        
        Args:
            order_id (int): Het ID van de bestelling om bij te werken.
            items (list): De bijgewerkte lijst met items binnen de bestelling.
        """
        order = self.get_order(order_id)
        current = order["items"]

        # Verwijder items die niet meer in de bestelling zijn
        for x in current:
            found = False
            for y in items:
                if x["item_id"] == y["item_id"]:
                    found = True
                    break
            if not found:
                inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(x["item_id"])
                min_ordered = 1_000_000_000_000_000_000
                min_inventory
                for z in inventories:
                    if z["total_allocated"] > min_ordered:
                        min_ordered = z["total_allocated"]
                        min_inventory = z
                min_inventory["total_allocated"] -= x["amount"]
                min_inventory["total_expected"] = y["total_on_hand"] + y["total_ordered"]
                data_provider.fetch_inventory_pool().update_inventory(min_inventory["id"], min_inventory)

        # Voeg of update items die in de bestelling zijn
        for x in current:
            for y in items:
                if x["item_id"] == y["item_id"]:
                    inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(x["item_id"])
                    min_ordered = 1_000_000_000_000_000_000
                    min_inventory
                    for z in inventories:
                        if z["total_allocated"] < min_ordered:
                            min_ordered = z["total_allocated"]
                            min_inventory = z
                min_inventory["total_allocated"] += y["amount"] - x["amount"]
                min_inventory["total_expected"] = y["total_on_hand"] + y["total_ordered"]
                data_provider.fetch_inventory_pool().update_inventory(min_inventory["id"], min_inventory)

        order["items"] = items
        self.update_order(order_id, order)

    def update_orders_in_shipment(self, shipment_id, orders):
        """Werk de zending bij door orders toe te voegen of te verwijderen van een zending.
        
        Args:
            shipment_id (int): Het ID van de zending.
            orders (list): Een lijst met order-ID's die bij de zending horen.
        """
        packed_orders = self.get_orders_in_shipment(shipment_id)
        for x in packed_orders:
            if x not in orders:
                order = self.get_order(x)
                order["shipment_id"] = -1
                order["order_status"] = "Scheduled"
                self.update_order(x, order)

        for x in orders:
            order = self.get_order(x)
            order["shipment_id"] = shipment_id
            order["order_status"] = "Packed"
            self.update_order(x, order)

    def remove_order(self, order_id):
        """Verwijdert een bestelling uit de data op basis van het order-ID.
        
        Args:
            order_id (int): Het ID van de bestelling om te verwijderen.
        """
        for x in self.data:
            if x["id"] == order_id:
                self.data.remove(x)

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
        """Saves the current data to the JSON file."""
        f = open(self.data_path, "w")
        json.dump(self.data, f)
