# import json
from providers import data_provider, auth_provider
from handlers import get_requests


def delete_object(self, path, user):
    # Melisa ik doe dit even hier als je klaar bent kan je verwijderen en je
    # eigen methode in de main stoppen
    if not auth_provider.has_access(user, path, "delete"):
        self.send_response(403)
        self.end_headers()
        return
    if path[0] == "warehouses":
        warehouse_id = int(path[1])
        data_provider.fetch_warehouse_pool().remove_warehouse(warehouse_id)
        data_provider.fetch_warehouse_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "locations":
        location_id = int(path[1])
        data_provider.fetch_location_pool().remove_location(location_id)
        data_provider.fetch_location_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "transfers":
        transfer_id = int(path[1])
        data_provider.fetch_transfer_pool().remove_transfer(transfer_id)
        data_provider.fetch_transfer_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "items":
        item_id = path[1]
        data_provider.fetch_item_pool().remove_item(item_id)
        data_provider.fetch_item_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "item_lines":
        item_line_id = int(path[1])
        data_provider.fetch_item_line_pool().remove_item_line(item_line_id)
        data_provider.fetch_item_line_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "item_groups":
        item_group_id = int(path[1])
        data_provider.fetch_item_group_pool().remove_item_group(item_group_id)
        data_provider.fetch_item_group_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "item_types":
        item_type_id = int(path[1])
        data_provider.fetch_item_type_pool().remove_item_type(item_type_id)
        data_provider.fetch_item_type_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "inventories":
        inventory_id = int(path[1])
        data_provider.fetch_inventory_pool().remove_inventory(inventory_id)
        data_provider.fetch_inventory_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "suppliers":
        supplier_id = int(path[1])
        data_provider.fetch_supplier_pool().remove_supplier(supplier_id)
        data_provider.fetch_supplier_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "orders":
        order_id = int(path[1])
        data_provider.fetch_order_pool().remove_order(order_id)
        data_provider.fetch_order_pool().save()
        self.send_response(200)
        self.end_headers()
    elif path[0] == "clients":
        client_id = int(path[1])
        RemoveClient = data_provider.fetch_client_pool(
        ).remove_client(client_id)
        data_provider.fetch_client_pool().save()
        get_requests.Call_json_response(self, RemoveClient)
        self.end_headers()
    elif path[0] == "shipments":
        shipment_id = int(path[1])
        data_provider.fetch_shipment_pool().remove_shipment(shipment_id)
        data_provider.fetch_shipment_pool().save()
        self.send_response(200)
        self.end_headers()
    else:
        self.send_response(404)
        self.end_headers()


def handle_delete_resource(self, resource_type, resource_id):
    collection = {
        "warehouses": (data_provider.fetch_warehouse_pool(), "remove_warehouse"),
        "locations": (data_provider.fetch_location_pool(), "remove_location"),
        "transfers": (data_provider.fetch_transfer_pool(), "remove_transfer"),
        "items": (data_provider.fetch_item_pool(), "remove_item"),
        "item_lines": (data_provider.fetch_item_line_pool(), "remove_item_line"),
        "item_groups": (data_provider.fetch_item_group_pool(),
                        "remove_item_group"),
        "item_types": (data_provider.fetch_item_type_pool(), "remove_item_type"),
        "inventories": (data_provider.fetch_inventory_pool(),
                        "remove_inventory"),
        "suppliers": (data_provider.fetch_supplier_pool(), "remove_supplier"),
        "orders": (data_provider.fetch_order_pool(), "remove_order"),
        "clients": (data_provider.fetch_client_pool(), "remove_client"),
        "shipments": (data_provider.fetch_shipment_pool(), "remove_shipment")
    }

    pool, removal_method_name = collection.get(resource_type)
    if pool:
        getattr(pool, removal_method_name)(resource_id)
        pool.save()
        self.send_response(200)
        self.end_headers()
    else:
        self.send_response(404)
        self.end_headers()
