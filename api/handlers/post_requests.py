from providers import data_provider
from handlers import get_requests
import json


class PostRequests():

    def Response(self, data):
        get_requests.Call_json_response(self, data)

    def ChoosePath(self, path):
        if path == "clients":
            PostRequests.post_object(self, data_provider.fetch_client_pool().add_client, data_provider.fetch_client_pool().save)
        elif path == "inventories":
            PostRequests.post_object(self, data_provider.fetch_inventory_pool().add_inventory, data_provider.fetch_inventory_pool().save)
        elif path == "item_groups":
            PostRequests.post_object(self, data_provider.fetch_item_group_pool().add_item_group, data_provider.fetch_item_group_pool().save)
        elif path == "item_lines":
            PostRequests.post_object(self, data_provider.fetch_item_line_pool().add_item_line, data_provider.fetch_item_line_pool().save) 
        elif path == "item_types": 
            PostRequests.post_object(self, data_provider.fetch_item_type_pool().add_item_type, data_provider.fetch_item_type_pool().save)
        elif path == "items":
            PostRequests.post_object(self, data_provider.fetch_item_pool().add_item, data_provider.fetch_item_pool().save)
        elif path == "locations":
            PostRequests.post_object(self, data_provider.fetch_location_pool().add_location, data_provider.fetch_location_pool().save) 
        elif path == "orders":
            PostRequests.post_object(self, data_provider.fetch_order_pool().add_order, data_provider.fetch_order_pool().save) 
        elif path == "shipments":
            PostRequests.post_object(self, data_provider.fetch_shipment_pool().add_shipment, data_provider.fetch_shipment_pool().save)
        elif path == "suppliers":
            PostRequests.post_object(self, data_provider.fetch_supplier_pool().add_supplier, data_provider.fetch_supplier_pool().save) 
        elif path == "transfers":
            PostRequests.post_object(self, data_provider.fetch_transfer_pool().add_transfer, data_provider.fetch_transfer_pool().save)
        elif path == "warehouses":
            PostRequests.post_object(self, data_provider.fetch_warehouse_pool().add_warehouse, data_provider.fetch_warehouse_pool().save)       
        else:
            self.send_response(404)
            self.end_headers()
  
    def post_object(self, AddObjectMethod, SaveObjectMethod):
        content_length = int(self.headers["Content-length"])
        post_data = self.rfile.read(content_length)
        new_object = json.loads(post_data.decode())
        Status = AddObjectMethod(new_object)
        SaveObjectMethod()
        PostRequests.Response(self, Status)
        self.end_headers()