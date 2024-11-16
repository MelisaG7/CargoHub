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
    _orders = Orders()(ROOT_PATH, DEBUG)
    global _clients
    _clients = Clients(ROOT_PATH, DEBUG)
    global _shipments
    _shipments = Shipments()(ROOT_PATH, DEBUG)

# With pool they mean that this object contains functions,
# that can retrieve, update, delete, add data to the Warehouse database.


def Orders():
    from models.orders import Orders
    return Orders


def Shipments():
    from models.shipments import Shipments
    return Shipments


def fetch_warehouse_pool():
    # This method returns an object of the class Warehouses.
    return _warehouses


def fetch_location_pool():
    # Returns an object of type Locations
    return _locations


def fetch_transfer_pool():
    # Returns an object of type Transfers
    return _transfers


def fetch_item_pool():
    # Returns and object of type Items
    return _items


def fetch_item_line_pool():
    # Returns an object of type ItemLines
    return _item_lines


def fetch_item_group_pool():
    # Returns an object of type ItemGroups
    return _item_groups


def fetch_item_type_pool():
    # Returns an object of type ItemTypes
    return _item_types


def fetch_inventory_pool():
    # Returns an object of type Inventories
    return _inventories


def fetch_supplier_pool():
    # Returns an object of type Suppliers
    return _suppliers


def fetch_order_pool():
    # Returns an object of type Orders
    return _orders


def fetch_client_pool():
    # Returns an object of type Clients
    return _clients


def fetch_shipment_pool():
    # Returns an object of type Shipments
    return _shipments
