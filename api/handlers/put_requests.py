from providers import data_provider
from handlers import get_requests
from processors import notification_processor
import json


class PutRequests:

    def Response(self, data):
        # Centralized response method
        get_requests.Call_json_response(self, data)

    def ChoosePath(self, path):
        # Leave this method unchanged
        if path[0] == "clients":
            PutRequests.put_object(self, path, data_provider.fetch_client_pool().update_client, data_provider.fetch_client_pool().save)
        elif path[0] == "inventories":
            PutRequests.put_object(self, path, data_provider.fetch_inventory_pool().update_inventory, data_provider.fetch_inventory_pool().save)
        elif path[0] == "item_groups":
            PutRequests.put_object(self, path, data_provider.fetch_item_group_pool().update_item_group, data_provider.fetch_item_group_pool().save)
        elif path[0] == "item_lines":
            PutRequests.put_object(self, path, data_provider.fetch_item_line_pool().update_item_line, data_provider.fetch_item_line_pool().save) 
        elif path[0] == "item_types": 
            PutRequests.put_object(self, path, data_provider.fetch_item_type_pool().update_item_type, data_provider.fetch_item_type_pool().save)
        elif path[0] == "items":
            PutRequests.put_object(self, path, data_provider.fetch_item_pool().update_item, data_provider.fetch_item_pool().save)
        elif path[0] == "locations":
            PutRequests.put_object(self, path, data_provider.fetch_location_pool().update_location, data_provider.fetch_location_pool().save) 
        elif path[0] == "orders":
            PutRequests.put_object(self, path, data_provider.fetch_order_pool().update_order, data_provider.fetch_order_pool().save) 
        elif path[0] == "shipments":
            PutRequests.put_object(self, path, data_provider.fetch_shipment_pool().update_shipment, data_provider.fetch_shipment_pool().save)
        elif path[0] == "suppliers":
            PutRequests.put_object(self, path, data_provider.fetch_supplier_pool().update_supplier, data_provider.fetch_supplier_pool().save) 
        elif path[0] == "transfers":
            PutRequests.put_object(self, path, data_provider.fetch_transfer_pool().update_transfer, data_provider.fetch_transfer_pool().save)
        elif path[0] == "warehouses":
            PutRequests.put_object(self, path, data_provider.fetch_warehouse_pool().update_warehouse, data_provider.fetch_warehouse_pool().save)       
        else:
            self.send_response(404)
            self.end_headers()

    def put_object(self, path, update_method, save_method):
        # Centralized put_object method for all paths
        try:
            object_id = int(path[1])
            content_length = int(self.headers["Content-length"])
            put_data = self.rfile.read(content_length)
            updated_object = json.loads(put_data.decode())

            # Handle updates with additional logic for specific cases
            if len(path) == 3:
                if path[2] == "items" and path[0] == "shipments":
                    update_method = data_provider.fetch_shipment_pool().update_items_in_shipment
                elif path[2] == "items" and path[0] == "orders":
                    update_method = data_provider.fetch_order_pool().update_items_in_order
                elif path[2] == "commit" and path[0] == "transfers":
                    self.process_transfer_commit(path)
                    return
                else:
                    self.send_response(404)
                    self.end_headers()
                    return

            # Update the object and save changes
            status = update_method(object_id, updated_object)
            save_method()
            PutRequests.Response(self, status)
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            print(f"Error processing PUT request: {e}")

    def process_transfer_commit(self, path):
        # Specific processing logic for transfer commits
        try:
            transfer_id = int(path[1])
            transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
            for item in transfer["items"]:
                inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(item["item_id"])
                for inventory in inventories:
                    if inventory["location_id"] == transfer["transfer_from"]:
                        inventory["total_on_hand"] -= item["amount"]
                    elif inventory["location_id"] == transfer["transfer_to"]:
                        inventory["total_on_hand"] += item["amount"]
                    inventory["total_expected"] = inventory["total_on_hand"] + inventory["total_ordered"]
                    inventory["total_available"] = inventory["total_on_hand"] - inventory["total_allocated"]
                    data_provider.fetch_inventory_pool().update_inventory(inventory["id"], inventory)
            transfer["transfer_status"] = "Processed"
            notification_processor.push(
                f"Processed batch transfer with id:{transfer['id']}")
            status = data_provider.fetch_transfer_pool().update_transfer(transfer_id, transfer)
            PutRequests.Response(self, status)
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            print(f"Error processing transfer commit: {e}")
