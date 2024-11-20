# Imports all classes from the files in the 'models' folder
from models.warehouses import Warehouses
from models.locations import Locations
from models.transfers import Transfers
from models.items import Items
from models.item_lines import ItemLines
from models.item_groups import ItemGroups
from models.item_types import ItemTypes
from models.inventories import Inventories
from models.suppliers import Suppliers
# from models.orders import Orders
from models.clients import Clients
# from models.shipments import Shipments

# constant boolean set to False
DEBUG = False

# Constant string.
ROOT_PATH = "./data/"

# Create variables. These are assigned to none.
_warehouses = None
_locations = None
_transfers = None
_items = None
_item_lines = None
_item_groups = None
_item_types = None
_inventories = None
_suppliers = None
_orders = None
_shipments = None
_clients = None


def init():
    # create global variables that can be used within functions.

    # Functions can give it other values,
    # however then it would be treated as a local variable in that function
    # Meaning for the rest of the program the value stays the same.
    global _warehouses
    _warehouses = Warehouses(ROOT_PATH, DEBUG)
    global _locations
    _locations = Locations(ROOT_PATH, DEBUG)
    global _transfers
    _transfers = Transfers(ROOT_PATH, DEBUG)
    global _items
    _items = Items(ROOT_PATH, DEBUG)
    global _item_lines
    _item_lines = ItemLines(ROOT_PATH, DEBUG)
    global _item_groups
    _item_groups = ItemGroups(ROOT_PATH, DEBUG)
    global _item_types
    _item_types = ItemTypes(ROOT_PATH, DEBUG)
    global _inventories
    _inventories = Inventories(ROOT_PATH, DEBUG)
    global _suppliers
    _suppliers = Suppliers(ROOT_PATH, DEBUG)
    global _orders
    _orders = Orders(ROOT_PATH, DEBUG)
    global _clients
    _clients = Clients(ROOT_PATH, DEBUG)
    global _shipments
    _shipments = Shipments(ROOT_PATH, DEBUG)

# With pool they mean that this object contains functions,
# that can retrieve, update, delete, add data to the Warehouse database.


POOL_DICT = {
    'warehouses': lambda: _warehouses,
    'locations': lambda: _locations,
    'transfers': lambda: _transfers,
    'items': lambda: _items,
    'item_lines': lambda:  _item_lines,
    'item_groups': lambda: _item_groups,
    'item_types': lambda: _item_types,
    'inventories': lambda: _inventories,
    'suppliers': lambda: _suppliers,
    'orders': lambda: _orders,
    'clients': lambda: _clients,
    'shipments': lambda: _shipments
}


def Orders(root_path: str, is_debug: bool):
    from models.orders import Orders
    return Orders(root_path, is_debug)


def Shipments(root_path: str, is_debug: bool):
    from models.shipments import Shipments
    return Shipments(root_path, is_debug)


def fetch_pool(model: str):
    for model in POOL_DICT:
        return POOL_DICT[model]
    raise ValueError(f"Wrong pool name {model}")
