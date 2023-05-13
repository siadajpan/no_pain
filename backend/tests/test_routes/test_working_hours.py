import json

import pytest


def add_user_and_practice(client):
    # Add client
    data = {
        "first_name": "name",
        "last_name": "last_name",
        "email": "testemail@email.com",
        "password": "testing",
    }
    client.post(url="/users/create", content=json.dumps(data))
    # Add practice
    data = {
        "name": "practice1",
        "postcode": "4000",
        "city": "Test",
        "street": "test address",
        "street_number": "14",
    }
    client.post(url="/practices/create", content=json.dumps(data))


def test_create_working_hours(client):
    add_user_and_practice(client)

    # Test adding working hours
    data = {
        "user_id": "0",
        "practice_id": "0",
        "day_of_week": "Monday",
        "start_time": "10:00",
        "end_time": "14:00",
    }
    response = client.post(url="/working_hours/create", content=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["start_time"] == "10:00"
    assert response.json()["end_time"] == "14:00"


@pytest.mark.parametrize(
    "day_of_week,start_time,end_time",
    [
        ("Monday1", "10:00", "13:00"),
        ("Monday", "110:00", "13:00"),
        ("Monday", "10:00", "131:00"),
        ("Monday", "10:70", "13:00"),
        ("Monday", "10:00", "13:90"),
    ],
)
def test_create_working_hours_wrong_fields(client, day_of_week, start_time, end_time):
    add_user_and_practice(client)

    # Test adding working hours
    data = {
        "user_id": "0",
        "practice_id": "0",
        "day_of_week": day_of_week,
        "start_time": start_time,
        "end_time": end_time,
    }
    response = client.post(url="/working_hours/create", content=json.dumps(data))
    assert response.status_code == 422
