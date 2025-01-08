from pydantic import BaseModel


class Client(BaseModel):
    id: int
    name: str
    address: str
    city: str
    zip_code: str
    province: str
    country: str
    contact_name: str
    contact_phone: str
    contact_email: str

    # {"id": 1,
    #  "name": "Raymond Inc",
    # "address": "1296 Daniel Road Apt. 349",
    # "city": "Pierceview",
    # "zip_code": "28301",
    # "province": "Colorado",
    # "country": "United States",
    # "contact_name": "Bryan Clark",
    # "contact_phone": "242.732.3483x2573",
    # "contact_email": "robertcharles@example.net"


class Inventory(BaseModel):
    id: int
    item_id: str
    description: str
    item_reference: str
    locations: list
    total_on_hand: int
    total_ordered: int
    total_allocated: int
    total_available: int
    # {
    # "id": 1,
    # "item_id":"P000001",
    # "description":
    # "Face-to-face clear-thinking complexity",
    # "item_reference": "sjQ23408K",
    # "locations": [3211, 24700, 14123, 19538, 31071, 24701, 11606, 11817],
    # "total_on_hand": 262,
    # "total_expected": 0,
    # "total_ordered": 80,
    # "total_allocated": 41,
    # "total_available": 141


class ItemGroup(BaseModel):
    id: int
    name: str
    description: str

    # {
    # "id": 0,
    # "name": "Electronics",
    # "description": "",


class ItemLine(BaseModel):
    id: int
    name: str
    description: str
    # {"id": 0,
    # "name": "Tech Gadgets",
    # "description": "",


class ItemType(BaseModel):
    id: int
    name: str
    description: str
    # {"id": 0,
    # "name": "Laptop",
    # "description": "",


class Item(BaseModel):
    uid: str
    code: str
    description: str
    short_description: str
    upc_code: str
    model_number: str
    commodity_code: str
    item_line: int
    item_group: int
    item_type: int
    unit_purchase_quantity: int
    unit_order_quantity: int
    pack_order_quantity: int
    supplier_id: int
    supplier_code: str
    supplier_part_number: str

    '''
    {
        "uid": "P000001",
        "code": "sjQ23408K",
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
    }
    '''


class Location(BaseModel):
    id: int
    warehouse_id: int
    code: str
    name: str
    # {"id": 1,
    # "warehouse_id": 1,
    # "code": "A.1.0",
    # "name": "Row: A, Rack: 1, Shelf: 0"


class Order(BaseModel):
    id: int
    source_id: int
    order_date: str
    request_date: str
    reference: str
    reference_extra: str
    order_status: str
    notes: str
    shipping_notes: str
    picking_notes: str
    warehouse_id: int
    ship_to: str
    bill_to: str
    shipment_id: int
    total_amount: float
    total_discount: float
    total_tax: float
    total_surcharge: float
    items: list   # {item_id: str, amount: int}


class Shipment(BaseModel):
    id: int
    order_id: int
    source_id: int
    order_date: str
    request_date: str
    shipment_date: str
    shipment_type: str
    shipment_status: str
    notes: str
    carrier_code: str
    carrier_description: str
    service_code: str
    payment_type: str
    transfer_mode: str
    total_package_count: int
    total_package_weight: float
    items: list


class Supplier(BaseModel):
    id: int
    code: str
    name: str
    address: str
    city: str
    zip_code: str
    province: str
    country: str
    contact_name: str
    phonenumber: str
    reference: str


class Transfer(BaseModel):
    id: int
    reference: str
    transfer_from: int
    transfer_to: int
    transfer_status: str
    items: list
    ''''
    {
    "id": 1,
    "reference": "TR00001",
    "transfer_from": null,
    "transfer_to": 9229,
    "transfer_status": "Completed",
    "created_at": "2000-03-11T13:11:14Z",
    "updated_at": "2000-03-12T16:11:14Z",
    "items": [
        {
            "item_id": "P007435",
            "amount": 23
        }
    ]
    '''


class Warehouse(BaseModel):
    id: int
    code: str
    name: str
    address: str
    zip: str
    city: str
    province: str
    country: str
    contact: dict
    # {"id": 1,
    # "code": "YQZZNL56",

    # "name": "Heemskerk cargo hub",

    # "address": "Karlijndreef 281",
    # "zip": "4002 AS",
    # "city": "Heemskerk",
    # "province": "Friesland",
    # "country": "NL",
    # "contact": {
    # "name": "Fem Keijzer",
    # "phone": "(078) 0013363",
    # "email": "blamore@example.net"

    # },
