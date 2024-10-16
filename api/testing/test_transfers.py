import json
from models.transfers import *
import pytest

DUMMY_DATA = [
    {
        "id": 1,
        "reference": "T",
        "transfer_from": None,
        "transfer_to": 1,
        "transfer_status": "t",
        "created_at": "2000-03-11T13:11:14Z",
        "updated_at": "2024-09-25T12:55:16.578271Z",
        "items": [
            {
                "item_id": "P007435",
                "amount": 23
            }
        ]
    },
    {
        "id": 2,
        "reference": "TR00002",
        "transfer_from": 9229,
        "transfer_to": 9284,
        "transfer_status": "Completed",
        "created_at": "2017-09-19T00:33:14Z",
        "updated_at": "2017-09-20T01:33:14Z",
        "items": [
            {
                "item_id": "P007435",
                "amount": 23
            }
        ]
    },
    {
        "id": 3,
        "reference": "TR000001",
        "transfer_from": None,
        "transfer_to": 9229,
        "transfer_status": "Completed",
        "created_at": "2000-03-11T13:11:14Z",
        "updated_at": "2024-09-22T15:52:42.875439Z",
        "items": [
            {
                "item_id": "P007435",
                "amount": 23
            }
        ]
    },
    {
        "id": 4,
        "reference": "TR00004",
        "transfer_from": None,
        "transfer_to": 9239,
        "transfer_status": "Completed",
        "created_at": "2000-03-11T13:11:14Z",
        "updated_at": "2000-03-12T14:11:14Z",
        "items": []
    },
    {
        "id": 5,
        "reference": "TR00005",
        "transfer_from": None,
        "transfer_to": 9191,
        "transfer_status": "Completed",
        "created_at": "2000-03-11T13:11:14Z",
        "updated_at": "2000-03-12T17:11:14Z",
        "items": [
            {
                "item_id": "P010015",
                "amount": 16
            }
        ]
    }
]

# Create an instance of the Transfers class and set dummy data
transfers = Transfers(".data/", True)
transfers.data = DUMMY_DATA


def test_get_transfers():
    # Checking if the database has been correctly set to the dummy_data
    result = transfers.get_transfers()
    assert len(result) == 5
    assert result[0]["reference"] == "T"


def test_get_transfer():
    # Checking if it returns None for a non-existing transfer
    result = transfers.get_transfer(10)
    assert result is None

    # Checking if the retrieved transfer is correct
    result = transfers.get_transfer(2)
    assert result["reference"] == "TR00002"


def test_get_items_in_transfer():
    # Checking if it returns None for a transfer without items
    result = transfers.get_items_in_transfer(4)
    assert result == []

    # Checking if the retrieved transfer is correct
    result = transfers.get_items_in_transfer(5)
    assert result == [{
        "item_id": "P010015",
        "amount": 16
    }]


def test_add_transfer():
    new_transfer = {
        "id": 6,
        "reference": "TR00006",
        "transfer_from": None,
        "transfer_to": 9252,
        "transfer_status": "Completed",
        "created_at": "2000-03-11T13:11:14Z",
        "updated_at": "2000-03-12T14:11:14Z",
        "items": [
            {
                "item_id": "P002084",
                "amount": 33
            }
        ]
    }
    transfers.add_transfer(new_transfer)
    result = transfers.get_transfer(6)
    assert result is not None
    assert result["transfer_to"] == 9252


def test_update_transfer():
    updated_transfer = {
        "id": 2,
        "reference": "TR00002-Updated",
        "transfer_from": 9229,
        "transfer_to": 9284,
        "transfer_status": "Completed",
        "created_at": "2017-09-19T00:33:14Z",
        # Assuming this method gets the current timestamp
        "updated_at": transfers.get_timestamp(),
        "items": [
            {
                "item_id": "P007435",
                "amount": 25
            }
        ]
    }
    transfers.update_transfer(2, updated_transfer)
    result = transfers.get_transfer(2)
    assert result["reference"] == "TR00002-Updated"
    assert result["items"][0]["amount"] == 25
    # Check if updated timestamp is current
    assert result["updated_at"] == updated_transfer["updated_at"]


def test_remove_transfer():
    # Check if transfer is correctly removed
    initial_count = len(transfers.data)
    transfers.remove_transfer(3)
    result = transfers.get_transfer(3)
    assert result is None
    assert len(transfers.data) == (initial_count - 1)
