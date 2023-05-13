import json

import pytest


@pytest.mark.parametrize("apartment_number", ["150", ""])
def test_create_practice(client, apartment_number):
    data = {
        "name": "practice1",
        "postcode": "5000",
        "city": "Test",
        "street": "test address",
        "street_number": "14",
        "apartment_number": apartment_number,
    }
    response = client.post(url="/practices/create", content=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["name"] == "practice1"
    assert response.json()["postcode"] == "5000"
    assert response.json()["city"] == "Test"
    assert response.json()["street"] == "test address"
    assert response.json()["street_number"] == "14"
    assert response.json()["apartment_number"] == apartment_number


def test_create_user(client):
    data = {
        "name": "practice1",
        "postcode": "5000",
        "city": "Test",
        "street": "test address",
        "street_number": "14",
        "apartment_number": "4",
    }
    response = client.post(url="/practices/create", content=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["name"] == "practice1"
    assert response.json()["postcode"] == "5000"
    assert response.json()["city"] == "Test"
    assert response.json()["street"] == "test address"
    assert response.json()["street_number"] == "14"
    assert response.json()["apartment_number"] == "4"


def test_read_practice(client):
    data = {
        "name": "practice1",
        "postcode": "5000",
        "city": "Test",
        "street": "test address",
        "street_number": "14",
        "apartment_number": "4",
    }
    client.post(url="/practices/create", content=json.dumps(data))
    response = client.get(url="/practices/get/1")
    assert response.status_code == 200
    assert response.json()["name"] == "practice1"
