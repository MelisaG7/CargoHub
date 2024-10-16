import json
from models.suppliers import *
import pytest


DUMMY_DATA = [{
    "id": 2,
    "code": "SUP0002",
            "name": "Testsupply",
            "address": "576 Christopher Roads",
            "address_extra": "Suite 072",
            "city": "Amberbury",
            "zip_code": "16105",
            "province": "Illinois",
            "country": "Saint Martin",
            "contact_name": "Kathleen Vincent",
            "phonenumber": "001-733-291-8848x3542",
            "reference": "H-SUP0002",
            "created_at": "1995-12-18 03:05:46",
            "updated_at": "2019-11-10 22:11:12"
},
    {
    "id": 3,
    "code": "SUP0003",
            "name": "White and Sons",
            "address": "1761 Shepard Valley",
            "address_extra": "Suite 853",
            "city": "Aguilarton",
            "zip_code": "63918",
            "province": "Wyoming",
            "country": "Ghana",
            "contact_name": "Jason Hudson",
            "phonenumber": "001-910-585-6962x8307",
            "reference": "WaS-SUP0003",
            "created_at": "2010-06-14 02:32:58",
            "updated_at": "2019-06-16 19:29:49"
},
    {
    "id": 4,
    "code": "SUP0004",
            "name": "Walker-Collins",
            "address": "847 Shannon Cape Suite 792",
            "address_extra": "Suite 011",
            "city": "Foleychester",
            "zip_code": "96720",
            "province": "Georgia",
            "country": "Guadeloupe",
            "contact_name": "Dr. Steven Graham",
            "phonenumber": "635-808-1014",
            "reference": "W-SUP0004",
            "created_at": "2004-01-17 11:07:39",
            "updated_at": "2013-07-05 10:49:28"
},
    {
    "id": 5,
    "code": "SUP0005",
            "name": "Davis Group",
            "address": "9407 Braun Mills Suite 802",
            "address_extra": "Apt. 401",
            "city": "Hansenberg",
            "zip_code": "36208",
            "province": "Illinois",
            "country": "Guinea",
            "contact_name": "Amanda Johnson",
            "phonenumber": "(814)854-5201",
            "reference": "DG-SUP0005",
            "created_at": "1978-08-30 07:34:20",
            "updated_at": "2013-03-16 07:34:36"
},
    {
    "id": 6,
    "code": "SUP0006",
            "name": "Martin PLC",
            "address": "243 Henry Station Suite 090",
            "address_extra": "Suite 011",
            "city": "Smithview",
            "zip_code": "48427",
            "province": "New York",
            "country": "Guadeloupe",
            "contact_name": "James Mills MD",
            "phonenumber": "001-763-501-5416x14812",
            "reference": "MP-SUP0006",
            "created_at": "2019-10-28 00:58:28",
            "updated_at": "2019-12-28 10:23:09"
}]

suppliers = Suppliers(".data/", True)
suppliers.data = DUMMY_DATA


def test_get_suppliers():
    # checking if the database has been correctly set to the dummy_data
    result = suppliers.get_suppliers()
    assert len(result) == 5
    assert result[0]["name"] == "Testsupply"


def test_get_supplier():
    # checking if it returns none to a non-existing supplier
    result = suppliers.get_supplier(1)
    assert result is None
    result = suppliers.get_supplier(2)
    assert result["code"] == "SUP0002"
    #  checking if the supplier it retrieved is correct


def test_add_supplier():
    new_supplier = {
        "id": 7,
        "code": "SUP0006",
        "name": "Added supplier PLC",
        "address": "243 Henry Station Suite 090",
        "address_extra": "Suite 011",
        "city": "Wijnhaven",
        "zip_code": "48427",
        "province": "New York",
        "country": "Guadeloupe",
        "contact_name": "James Mills MD",
        "phonenumber": "001-763-501-5416x14812",
        "reference": "MP-SUP0006",
        "created_at": "2019-10-28 00:58:28",
        "updated_at": "2019-12-28 10:23:09"
    }
    suppliers.add_supplier(new_supplier)
    result = suppliers.get_supplier(7)
    assert result is not None
    assert result["city"] == "Wijnhaven"


def test_update_supplier():
    updated_supplier = new_supplier = {
        "id": 7,
        "code": "SUP0006",
        "name": "Updated supplier PLC",
        "address": "243 Henry Station Suite 090",
        "address_extra": "Suite 011",
        "city": "Wijnhaven",
        "zip_code": "48427",
        "province": "New York",
        "country": "Guadeloupe",
        "contact_name": "James Mills MD",
        "phonenumber": "001-763-501-5416x14812",
        "reference": "MP-SUP0006",
        "created_at": "2019-10-28 00:58:28",
        "updated_at": "2019-12-28 10:23:09"
    }
    suppliers.update_supplier(7, updated_supplier)
    time = suppliers.get_timestamp()

    result = suppliers.get_supplier(7)
    assert result["name"] == "Updated supplier PLC"
    assert result["updated_at"] == time
    # check if time updated correctly


def test_remove_supplier():
    # check if correctly removed
    amount_suppliers = len(suppliers.data)
    suppliers.remove_supplier(4)

    result = suppliers.get_supplier(4)
    assert result is None
    assert len(suppliers.data) == (amount_suppliers - 1)
