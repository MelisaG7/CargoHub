import pytest
from models.warehouses import *

DUMMY_DATA = [
    {
        "id": 190,
        "code": "t",
        "name": "Tested longterm hub",
        "address": "t",
        "zip": "t",
        "city": "t",
        "province": "t",
        "country": "t",
        "contact": {
            "name": "t",
            "phone": "t",
            "email": "t"
        },
        "created_at": "2024-09-25T12:00:42.083724Z",
        "updated_at": "2024-09-25T12:47:21.516387Z"
    },
    {
        "id": 3,
        "code": "TTVCKINLLK",
        "name": "TTNaaldwijk distribution hub",
        "address": "TTT 807",
        "zip": "TT",
        "city": "TESTCITY",
        "province": "T",
        "country": "T",
        "contact": {
            "name": "TTFrederique van Wallaert",
            "phone": "TT(009) 4870289",
            "email": "TTjelle66@example.net"
        },
        "created_at": "2001-05-11 10:43:52",
        "updated_at": "2024-09-18T12:35:58.709455Z"
    },
    {
        "id": 4,
        "code": "IPJMNLSY",
        "name": "Bosch en Duin storage location",
        "address": "Fabianweg 71",
        "zip": "5701 IA",
        "city": "Bosch en Duin",
        "province": "Flevoland",
        "country": "NL",
        "contact": {
            "name": "Oscar Hemma van Allemanië-Hoes",
            "phone": "058 2995479",
            "email": "suze00@example.org"
        },
        "created_at": "2007-10-19 09:43:20",
        "updated_at": "2019-11-02 07:30:52"
    },
    {
        "id": 5,
        "code": "QAQMNLCL",
        "name": "Hoogeveen distribution facility",
        "address": "Noaboulevard 7",
        "zip": "1735XO",
        "city": "Hoogeveen",
        "province": "Zuid-Holland",
        "country": "NL",
        "contact": {
            "name": "Sjoerd Sterkman",
            "phone": "0943-736616",
            "email": "imkehermans@example.org"
        },
        "created_at": "2017-11-03 19:21:26",
        "updated_at": "2023-05-30 16:45:10"
    }
]

warehouses = Warehouses(".data/", True)
warehouses.data = DUMMY_DATA


def test_get_warehouses():
    # Check if the database has been correctly set to the dummy_data
    result = warehouses.get_warehouses()
    assert len(result) == 4
    assert result[0]["name"] == "Tested longterm hub"


def test_get_warehouse():
    # Check if it returns None for a non-existing warehouse
    result = warehouses.get_warehouse(999)
    assert result is None

    # Check if the warehouse retrieved is correct
    result = warehouses.get_warehouse(190)
    assert result["code"] == "t"


def test_add_warehouse():
    new_warehouse = {
        "id": 6,
        "code": "NEWCODE",
        "name": "New Warehouse",
        "address": "New Street 123",
        "zip": "12345",
        "city": "NewCity",
        "province": "NewProvince",
        "country": "NewCountry",
        "contact": {
            "name": "New Contact",
            "phone": "1234567890",
            "email": "newcontact@example.com"
        },
        "created_at": "2024-10-13T00:00:00Z",
        "updated_at": "2024-10-13T00:00:00Z"
    }
    warehouses.add_warehouse(new_warehouse)
    result = warehouses.get_warehouse(6)
    assert result is not None
    assert result["city"] == "NewCity"


def test_update_warehouse():
    updated_warehouse = {
        "id": 6,
        "code": "NEWCODE",
        "name": "Updated Warehouse",
        "address": "Updated Street 123",
        "zip": "54321",
        "city": "UpdatedCity",
        "province": "UpdatedProvince",
        "country": "UpdatedCountry",
        "contact": {
            "name": "Updated Contact",
            "phone": "0987654321",
            "email": "updatedcontact@example.com"
        },
        "created_at": "2024-10-13T00:00:00Z",
        "updated_at": "2024-10-13T12:00:00Z"
    }
    warehouses.update_warehouse(6, updated_warehouse)
    time = warehouses.get_timestamp()

    result = warehouses.get_warehouse(6)
    assert result["name"] == "Updated Warehouse"
    assert result["updated_at"] == time
    # Check if the time was updated correctly


def test_remove_warehouse():
    # Check if a warehouse is correctly removed
    amount_warehouses = len(warehouses.data)
    warehouses.remove_warehouse(4)

    result = warehouses.get_warehouse(4)
    assert result is None
    assert len(warehouses.data) == (amount_warehouses - 1)
