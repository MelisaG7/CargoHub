import pytest
from services.shipments import Shipments
from models.Models import Shipment, Item

SHIPMENTS = [
    {
        "id": 1,
        "order_id": 1,
        "source_id": 33,
        "order_date": "2000-03-09",
        "request_date": "2000-03-11",
        "shipment_date": "2000-03-13",
        "shipment_type": "I",
        "shipment_status": "Pending",
        "notes": "Zee vertrouwen klas rots heet lachen oneven begrijpen.",
        "carrier_code": "DPD",
        "carrier_description": "Dynamic Parcel Distribution",
        "service_code": "Fastest",
        "payment_type": "Manual",
        "transfer_mode": "Ground",
        "total_package_count": 31,
        "total_package_weight": 594.42,
        "created_at": "2000-03-10T11:11:14Z",
        "updated_at": "2000-03-11T13:11:14Z",
        "items": [
            {
                "item_id": "P007435",
                "amount": 23
            },
            {
                "item_id": "P009557",
                "amount": 1
            }
        ]
    },{
        "id": 2,
        "order_id": 2,
        "source_id": 9,
        "order_date": "1983-11-28",
        "request_date": "1983-11-30",
        "shipment_date": "1983-12-02",
        "shipment_type": "I",
        "shipment_status": "Transit",
        "notes": "Wit duur fijn vlieg.",
        "carrier_code": "PostNL",
        "carrier_description": "Royal Dutch Post and Parcel Service",
        "service_code": "TwoDay",
        "payment_type": "Automatic",
        "transfer_mode": "Ground",
        "total_package_count": 56,
        "total_package_weight": 42.25,
        "created_at": "1983-11-29T11:12:17Z",
        "updated_at": "1983-11-30T13:12:17Z",
        "items": [
            {
                "item_id": "P003790",
                "amount": 10
            },
            {
                "item_id": "P007369",
                "amount": 15
            }
]}, {
        "id": 3,
        "order_id": 3,
        "source_id": 52,
        "order_date": "1973-01-28",
        "request_date": "1973-01-30",
        "shipment_date": "1973-02-01",
        "shipment_type": "I",
        "shipment_status": "Pending",
        "notes": "Hoog genot springen afspraak mond bus.",
        "carrier_code": "DHL",
        "carrier_description": "DHL Express",
        "service_code": "NextDay",
        "payment_type": "Automatic",
        "transfer_mode": "Ground",
        "total_package_count": 29,
        "total_package_weight": 463.0,
        "created_at": "1973-01-28T20:09:11Z",
        "updated_at": "1973-01-29T22:09:11Z",
        "items": [
            {
                "item_id": "P010669",
                "amount": 16
            }
        ]
    } ]

# Testen voor de Shipments class
def test_get_shipments():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()  # Mock data invoegen
    assert ship.get_shipments() == SHIPMENTS  # Controleer of we de juiste zendingen krijgen

def test_get_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    assert ship.get_shipment(1) == SHIPMENTS[0]  # Zending 1 ophalen

def test_add_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    shipment = Shipment(
    id=4,
    order_id=4,
    source_id=12,
    order_date="1980-05-09",
    request_date="1980-05-11",
    shipment_date="1980-05-13",
    shipment_type="I",
    shipment_status="Transit",
    notes="Oneven bloem brengen dubbel knie zorgen.",
    carrier_code="TNTexpress",
    carrier_description="TNT Express",
    service_code="Economy",
    payment_type="Automatic",
    transfer_mode="Ground",
    total_package_count=10,
    total_package_weight=688.01,
    created_at="1980-05-10T03:48:53Z",
    updated_at="1980-05-11T05:48:53Z",
    items=[
        {"item_id": "P007004", "amount": 14},
        {"item_id": "P005769", "amount": 28}
    ]
)
    ship.add_shipment(shipment)
    shipments = ship.get_shipments()
    assert len(shipments) == 4
    assert shipments[-1]["order_date"] =="1980-05-09"
    assert shipments[-1]["id"] == 4


def test_update_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    new_shipment = Shipment(
    id=6,
    order_id=4,
    source_id=12,
    order_date="1980-05-09",
    request_date="1980-05-11",
    shipment_date="1980-05-13",
    shipment_type="I",
    shipment_status="Transit",
    notes="Nieuwe shipment om update te testen",
    carrier_code="TNTexpress",
    carrier_description="TNT Express",
    service_code="Economy",
    payment_type="Automatic",
    transfer_mode="Ground",
    total_package_count=10,
    total_package_weight=688.01,
    created_at="1980-05-10T03:48:53Z",
    updated_at="1980-05-11T05:48:53Z",
    items=[
        {"item_id": "P007004", "amount": 14},
        {"item_id": "P005769", "amount": 28}
    ]
)
    ship.update_shipment(3, new_shipment)
    shipments = ship.get_shipments()
    assert len(shipments) == 3
    assert shipments[-1]["id"] == 6
    assert shipments[-1]["notes"] == "Nieuwe shipment om update te testen"



def test_remove_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    ship.remove_shipment(1)
    assert len(ship.data) == 2  # Controleer of de zending is verwijderd
    assert all(x["id"] != 1 for x in ship.data)  # Controleer of geen zending met id 1 meer bestaat

def test_get_items_in_shipment():
    ship = Shipments(root_path="", is_debug=True)
    ship.data = SHIPMENTS.copy()
    assert ship.get_items_in_shipment(1) == SHIPMENTS[0]["items"]  # Items in zending 1 ophalen
    # assert ship.get_items_in_shipment(999) is None  # Niet-bestaande zending moet None retourneren
