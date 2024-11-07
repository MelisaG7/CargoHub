import json
from providers import data_provider


def send_json_response(self, data, status=200):
    # This helper sends the data in json format back to the user with status 200
    self.send_response(status)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(data).encode("utf-8"))


def get_warehouses(self, path):
    # The path is the api-route example: http://localhost:3000/api/v1/warehouses, this method checks the length of the route and connect to the methods in the models
    # Which connects us to the data
    paths = len(path)
    match paths:
        case 1:
            warehouses = data_provider.fetch_warehouse_pool().get_warehouses()
            send_json_response(self, warehouses)
        case 2:
            warehouse_id = int(path[1])
            warehouse = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)
            send_json_response(self, warehouse)
        case 3:
            if path[2] == "locations":
                warehouse_id = int(path[1])
                locations = data_provider.fetch_location_pool(
                ).get_locations_in_warehouse(warehouse_id)
                send_json_response(self, locations)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_locations(self, path):
    paths = len(path)
    match paths:
        case 1:
            locations = data_provider.fetch_location_pool().get_locations()
            send_json_response(self, locations)
        case 2:
            location_id = int(path[1])
            location = data_provider.fetch_location_pool().get_location(location_id)
            send_json_response(self, location)
        case _:
            self.send_response(404)
            self.end_headers()


def get_transfers(self, path):
    paths = len(path)
    match paths:
        case 1:
            transfers = data_provider.fetch_transfer_pool().get_transfers()
            send_json_response(self, transfers)
        case 2:
            transfer_id = int(path[1])
            transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
            send_json_response(self, transfer)
        case 3:
            if path[2] == "items":
                transfer_id = int(path[1])
                items = data_provider.fetch_transfer_pool().get_items_in_transfer(transfer_id)
                send_json_response(self, items)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_items(self, path):
    paths = len(path)
    match paths:
        case 1:
            items = data_provider.fetch_item_pool().get_items()
            send_json_response(self, items)
        case 2:
            item_id = path[1]
            item = data_provider.fetch_item_pool().get_item(item_id)
            send_json_response(self, item)
        case 3:
            if path[2] == "inventory":
                item_id = path[1]
                inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(item_id)
                send_json_response(self, inventories)
            else:
                self.send_response(404)
                self.end_headers()
        case 4:
            if path[2] == "inventory" and path[3] == "totals":
                item_id = path[1]
                totals = data_provider.fetch_inventory_pool().get_inventory_totals_for_item(item_id)
                send_json_response(self, totals)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_item_lines(self, path):
    paths = len(path)
    print(paths, path)
    match paths:
        case 1:
            item_lines = data_provider.fetch_item_line_pool().get_item_lines()
            send_json_response(self, item_lines)
        case 2:
            item_line_id = int(path[1])
            item_line = data_provider.fetch_item_line_pool().get_item_line(item_line_id)
            send_json_response(self, item_line)
        case 3:
            if path[2] == "items":
                item_line_id = int(path[1])
                items = data_provider.fetch_item_pool().get_items_for_item_line(item_line_id)
                send_json_response(self, items)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_item_groups(self, path):
    paths = len(path)
    match paths:
        case 1:
            item_groups = data_provider.fetch_item_group_pool().get_item_groups()
            send_json_response(self, item_groups)
        case 2:
            item_group_id = int(path[1])
            item_group = data_provider.fetch_item_group_pool().get_item_group(item_group_id)
            send_json_response(self, item_group)
        case 3:
            if path[2] == "items":
                item_group_id = int(path[1])
                items = data_provider.fetch_item_pool().get_items_for_item_group(item_group_id)
                send_json_response(self, items)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_item_types(self, path):
    paths = len(path)
    match paths:
        case 1:
            item_types = data_provider.fetch_item_type_pool().get_item_types()
            send_json_response(self, item_types)
        case 2:
            item_type_id = int(path[1])
            item_type = data_provider.fetch_item_type_pool().get_item_type(item_type_id)
            send_json_response(self, item_type)
        case 3:
            if path[2] == "items":
                item_type_id = int(path[1])
                items = data_provider.fetch_item_pool().get_items_for_item_type(item_type_id)
                send_json_response(self, items)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_inventories(self, path):
    paths = len(path)
    match paths:
        case 1:
            inventories = data_provider.fetch_inventory_pool().get_inventories()
            send_json_response(self, inventories)
        case 2:
            inventory_id = int(path[1])
            inventory = data_provider.fetch_inventory_pool().get_inventory(inventory_id)
            send_json_response(self, inventory)
        case _:
            self.send_response(404)
            self.end_headers()


def get_suppliers(self, path):
    paths = len(path)
    match paths:
        case 1:
            suppliers = data_provider.fetch_supplier_pool().get_suppliers()
            send_json_response(self, suppliers)
        case 2:
            supplier_id = int(path[1])
            supplier = data_provider.fetch_supplier_pool().get_supplier(supplier_id)
            send_json_response(self, supplier)
        case 3:
            if path[2] == "items":
                supplier_id = int(path[1])
                items = data_provider.fetch_item_pool().get_items_for_supplier(supplier_id)
                send_json_response(self, items)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_orders(self, path):
    paths = len(path)
    match paths:
        case 1:
            orders = data_provider.fetch_order_pool().get_orders()
            send_json_response(self, orders)
        case 2:
            order_id = int(path[1])
            order = data_provider.fetch_order_pool().get_order(order_id)
            send_json_response(self, order)
        case 3:
            if path[2] == "items":
                order_id = int(path[1])
                items = data_provider.fetch_order_pool().get_items_in_order(order_id)
                send_json_response(self, items)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_clients(self, path):
    paths = len(path)
    match paths:
        case 1:
            clients = data_provider.fetch_client_pool().get_clients()
            send_json_response(self, clients)
        case 2:
            client_id = int(path[1])
            client = data_provider.fetch_client_pool().get_client(client_id)
            send_json_response(self, client)
        case 3:
            if path[2] == "orders":
                client_id = int(path[1])
                orders = data_provider.fetch_order_pool().get_orders_for_client(client_id)
                send_json_response(self, orders)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def get_shipments(self, path):
    paths = len(path)
    match paths:
        case 1:
            shipments = data_provider.fetch_shipment_pool().get_shipments()
            send_json_response(self, shipments)
        case 2:
            shipment_id = int(path[1])
            shipment = data_provider.fetch_shipment_pool().get_shipment(shipment_id)
            send_json_response(self, shipment)
        case 3:
            if path[2] == "orders":
                shipment_id = int(path[1])
                orders = data_provider.fetch_order_pool().get_orders_in_shipment(shipment_id)
                send_json_response(self, orders)
            elif path[2] == "items":
                shipment_id = int(path[1])
                items = data_provider.fetch_shipment_pool().get_items_in_shipment(shipment_id)
                send_json_response(self, items)
            else:
                self.send_response(404)
                self.end_headers()
        case _:
            self.send_response(404)
            self.end_headers()


def handle_get_request(self, path):
    # We check wether the first part of the route is valid and redirect to that part of the code
    api_route = path[0]
    if api_route == "warehouses":
        get_warehouses(self, path)
    elif api_route == "locations":
        get_locations(self, path)
    elif api_route == "transfers":
        get_transfers(self, path)
    elif api_route == "items":
        get_items(self, path)
    elif api_route == "item_lines":
        get_item_lines(self, path)
    elif api_route == "item_groups":
        get_item_groups(self, path)
    elif api_route == "item_types":
        get_item_types(self, path)
    elif api_route == "inventories":
        get_inventories(self, path)
    elif api_route == "suppliers":
        get_suppliers(self, path)
    elif api_route == "orders":
        get_orders(self, path)
    elif api_route == "clients":
        get_clients(self, path)
    elif api_route == "shipments":
        get_shipments(self, path)
    else:
        self.send_response(404)
        self.end_headers()
