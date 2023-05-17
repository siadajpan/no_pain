import json

import pytest


def create_practices(client, amount=1):
    for i in range(amount):
        data = {
            "email": f"test_email{i}@test.com",
            "password": "test_password",
            "name": f"practice{i}",
            "postcode": "5000",
            "city": "Test",
            "street": "test address",
            "street_number": f"{i}",
            "apartment_number": "4",
        }
        client.post(url="/practices/create", content=json.dumps(data))


@pytest.mark.parametrize("apartment_number", ["150", ""])
def test_create_practice(client, apartment_number):
    data = {
        "email": "test_email@test.com",
        "password": "test_password",
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


def test_read_practice(client):
    create_practices(client)
    response = client.get(url="/practices/get/1")
    assert response.status_code == 200
    assert response.json()["name"] == "practice0"


def test_read_practices(client):
    create_practices(client, amount=10)
    response = client.get(url="/practices/all")
    assert response.status_code == 200
    assert len(response.json()) == 10
