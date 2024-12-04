# Imports all classes from the files in the 'models' folder
from services.warehouses import Warehouses
from services.locations import Locations
from services.transfers import Transfers
from services.items import Items
from services.item_lines import ItemLines
from services.item_groups import ItemGroups
from services.item_types import ItemTypes
from services.inventories import Inventories
from services.suppliers import Suppliers
# from services.orders import Orders
from services.clients import Clients
# from services.shipments import Shipments

# constant boolean set to False
DEBUG = False

# Constant string.
ROOT_PATH = "./data/"

# Create variables. These are assigned to none.


def init():
    global _warehouses, _locations, _transfers, _items, _item_lines
    global _item_groups, _item_types, _inventories, _suppliers
    global _orders, _clients, _shipments

    _warehouses = Warehouses(ROOT_PATH, DEBUG)
    _locations = Locations(ROOT_PATH, DEBUG)
    _transfers = Transfers(ROOT_PATH, DEBUG)
    _items = Items(ROOT_PATH, DEBUG)
    _item_lines = ItemLines(ROOT_PATH, DEBUG)
    _item_groups = ItemGroups(ROOT_PATH, DEBUG)
    _item_types = ItemTypes(ROOT_PATH, DEBUG)
    _inventories = Inventories(ROOT_PATH, DEBUG)
    _suppliers = Suppliers(ROOT_PATH, DEBUG)
    _orders = Orders(ROOT_PATH, DEBUG)
    _clients = Clients(ROOT_PATH, DEBUG)
    _shipments = Shipments(ROOT_PATH, DEBUG)

    # Update POOL_DICT after initialization
    global POOL_DICT
    POOL_DICT = {
        'warehouses': _warehouses,
        'locations': _locations,
        'transfers': _transfers,
        'items': _items,
        'item_lines': _item_lines,
        'item_groups': _item_groups,
        'item_types': _item_types,
        'inventories': _inventories,
        'suppliers': _suppliers,
        'orders': _orders,
        'clients': _clients,
        'shipments': _shipments
    }


def Orders(root_path: str, is_debug: bool):
    from services.orders import Orders
    return Orders(root_path, is_debug)


# Order and shipment method to prevent circulair import

def Shipments(root_path: str, is_debug: bool):
    from services.shipments import Shipments
    return Shipments(root_path, is_debug)

# Calls the lambda in the dictionary op basis van key


def fetch_pool(model: str):
    if model in POOL_DICT:
        return POOL_DICT[model]
    raise ValueError(f"Wrong pool name {model}")
