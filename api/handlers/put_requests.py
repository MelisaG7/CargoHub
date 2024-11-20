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
        if path[0] in data_provider.POOL_DICT:
            PutRequests.put_object(
                self,
                path,
                data_provider.POOL_DICT[path[0]].update,
                data_provider.POOL_DICT[path[0]].save)
            return
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
                    update_method = data_provider.POOL_DICT["shipments"].update_items_in_shipment
                elif path[2] == "items" and path[0] == "orders":
                    update_method = data_provider.POOL_DICT["orders"].update_items_in_order
                elif path[2] == "commit" and path[0] == "transfers":
                    PutRequests.process_transfer_commit(path)
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
            transfer = data_provider.POOL_DICT["transfers"].get_transfer(transfer_id)
            for item in transfer["items"]:
                inventories = data_provider.POOL_DICT["inventories"].get_inventories_for_item(item["item_id"])
                for inventory in inventories:
                    if inventory["location_id"] == transfer["transfer_from"]:
                        inventory["total_on_hand"] -= item["amount"]
                    elif inventory["location_id"] == transfer["transfer_to"]:
                        inventory["total_on_hand"] += item["amount"]
                    inventory["total_expected"] = inventory["total_on_hand"] + inventory["total_ordered"]
                    inventory["total_available"] = inventory["total_on_hand"] - inventory["total_allocated"]
                    data_provider.POOL_DICT["inventories"].update(inventory["id"], inventory)
            transfer["transfer_status"] = "Processed"
            notification_processor.push(
                f"Processed batch transfer with id:{transfer['id']}")
            status = data_provider.POOL_DICT["transfers"].update(transfer_id, transfer)
            PutRequests.Response(self, status)
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            print(f"Error processing transfer commit: {e}")
