import json
from providers import data_provider

# The path is whatever is remaining after v1/ => for example http://localhost:3000/api/v1/shipments/10


def delete(self, path):
    # Items is the only one which doesn't use integer but uid > for example P000001
    if path[0] != "items":
        id = int(path[1])
    else:
        id = path[1]
    # Using a switch statement on the first part of the path we determine what we should do next
    match path[0]:
        case "warehouses":
            # If the path is recognized it will first go to the remove method of the class
            # Afterwards to the save method to save the changes in the database
            data_provider.fetch_warehouse_pool().remove_warehouse(id)
            data_provider.fetch_warehouse_pool().save()
        case "locations":
            data_provider.fetch_location_pool().remove_location(id)
            data_provider.fetch_location_pool().save()
        case "transfers":
            data_provider.fetch_transfer_pool().remove_transfer(id)
            data_provider.fetch_transfer_pool().save()
        case "items":
            data_provider.fetch_item_pool().remove_item(id)
            data_provider.fetch_item_pool().save()
        case "item_lines":
            data_provider.fetch_item_line_pool().remove_item_line(id)
            data_provider.fetch_item_line_pool().save()
        case "item_groups":
            data_provider.fetch_item_group_pool().remove_item_group(id)
            data_provider.fetch_item_group_pool().save()
        case "item_types":
            data_provider.fetch_item_type_pool().remove_item_type(id)
            data_provider.fetch_item_type_pool().save()
        case "inventories":
            data_provider.fetch_inventory_pool().remove_inventory(id)
            data_provider.fetch_inventory_pool().save()
        case "suppliers":
            data_provider.fetch_supplier_pool().remove_supplier(id)
            data_provider.fetch_supplier_pool().save()
        case  "orders":
            data_provider.fetch_order_pool().remove_order(id)
            data_provider.fetch_order_pool().save()
        case  "clients":
            data_provider.fetch_client_pool().remove_client(id)
            data_provider.fetch_client_pool().save()
        case "shipments":
            data_provider.fetch_shipment_pool().remove_shipment(id)
            data_provider.fetch_shipment_pool().save()
        case _:
            # If the path is non-existing it will send a 404 response back.
            self.send_response(404)  # Resource type not found
            self.end_headers()
            return
    # If everything went as supposed to, the response will be 200 OK.
    self.send_response(200)
    self.end_headers()
