import json
from providers import data_provider


def Call_json_response(self, data):
    if isinstance(data, tuple):
        send_json_response(self, data[0], data[1])
    else:
        send_json_response(self, data)


def send_json_response(self, status: int = 200, data: dict = None):
    # Heb ook ff dict and int erin gedaan bij parameters,
    # wanneer er alleen 2 parameters wordt gestuurd de methode weet welke is

    # Ik heb data optional gemaakt want als iets fout gaat wordt data niet gestuurd

    # Deze methode is hetzelfde als dei daarboven,
    # alleen wil ik die daarboven niet meteen refactoren
    # Dit ga ik temporarely gebruiken voor mn eigen methodes + voor het uittesten

    '''
    Oke dus wanneer wij een methode aanroepen (data),
    moet data wat teruggeven aan mij zodat ik weet welke response ik moet gaan sturen.

    Of data moet een getal teruggeven zoals 200 om dan gelijk een response te kunnen sturen.
    Ik denk dat ik daarvoor ga

    Plan:
    Laat get_client een methode terugsturen...+ een message? Maar hoe gaat dat dan precies?
    Laten we eerst maar een status code proberen te sturen
    '''
    # Dit domme ding denkt dat data 400 is maar het is de status eigenlijk
    self.send_response(status)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(data).encode("utf-8"))


def get_warehouses(self, path):
    # The path is the api-route example: warehouses/.../..., this method checks the length of the route and connect to the methods in the models
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
            Call_json_response(self, item_groups)
        case 2:
            item_group_id = int(path[1])
            item_group = data_provider.fetch_item_group_pool().get_item_group(item_group_id)
            Call_json_response(self, item_group)
        case 3:
            if path[2] == "items":
                item_group_id = int(path[1])
                items = data_provider.fetch_item_pool().get_items_for_item_group(item_group_id)
                Call_json_response(self, items)
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
            Call_json_response(self, inventories)
        case 2:
            inventory_id = int(path[1])
            inventory = data_provider.fetch_inventory_pool().get_inventory(inventory_id)
            Call_json_response(self, inventory)
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
    # path is clients/<client_id>/<orders>
    paths = len(path)
    match paths:
        case 1:
            # This calls the method 'get clients' in the class "Clients"
            clients = data_provider.POOL_DICT[path[0]].get_clients()
            # The status in the 'send_json_response' is always 200
            Call_json_response(self, clients)
        case 2:
            client_id = int(path[1])
            client = data_provider.fetch_client_pool().get_client(client_id)
            # Status sent is always 200 here too on default.
            # Oke dus 'get_client' moet een client object returnen EN status code. Ik doe dat even in een tuple ofzo
            # Je krijgt niet atlijd data, dus dat moet ook optional worden
            Call_json_response(self, client)
        case 3:
            # Als ik dit correct hebt begrepen is als de path 'clients/<client_id>/orders' is,
            # dan krijg je de order van de client
            if path[2] == "orders":
                client_id = int(path[1])
                orders = data_provider.fetch_order_pool().get_orders_for_client(client_id)
                send_json_response(self, orders)
            else:
                # Als path[2] wat anders is, krijg je 404 statuscode
                self.send_response(404)
                self.end_headers()
        case _:
            # Als je een andere case hebt, krijg je ook 404 statuscode
            # Aha. Dus als ik wil dat deze domme functies andere status codes weergeven, moet ik dat hier regelen
            # Hopefully I will cook. mhmmhmm
            # Het enige wat ik moet weten is wrm die send_json_response wordt gecalled..
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
    # path in mijn geval i sbijvoorbeeld: clients/.../...
    # If the user has access according to the first method in the main Get-version_1?? it calls this method:
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
        # In my case (Mawadda) it should then call get_clients():
        # The path would be: url/api/v1/clients? or url/api/v1/clients/<client_id>
    elif api_route == "clients":
        get_clients(self, path)
    elif api_route == "shipments":
        get_shipments(self, path)
    else:
        self.send_response(404)
        self.end_headers()
