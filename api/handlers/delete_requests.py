import json
from providers import data_provider


def handle_delete_resource(self, resource_type, resource_id):
    collection = {
        "warehouses": (data_provider.fetch_warehouse_pool(), "remove_warehouse"),
        "locations": (data_provider.fetch_location_pool(), "remove_location"),
        "transfers": (data_provider.fetch_transfer_pool(), "remove_transfer"),
        "items": (data_provider.fetch_item_pool(), "remove_item"),
        "item_lines": (data_provider.fetch_item_line_pool(), "remove_item_line"),
        "item_groups": (data_provider.fetch_item_group_pool(), "remove_item_group"),
        "item_types": (data_provider.fetch_item_type_pool(), "remove_item_type"),
        "inventories": (data_provider.fetch_inventory_pool(), "remove_inventory"),
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
