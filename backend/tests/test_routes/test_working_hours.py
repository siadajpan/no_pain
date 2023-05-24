import json

import pytest

from backend.tests.test_routes.test_doctors import create_test_doctors
from backend.tests.test_routes.test_practices import create_practices
from backend.tests.utils.users import user_authentication_headers


def add_working_hours(client, amount_users=1, amount_practices=1, amount_wh=1):
    users = create_test_doctors(client, amount_users)
    headers = [
        user_authentication_headers(
            client=client, email=user["email"], password=user["password"]
        )
        for user in users
    ]
    create_practices(client, amount_practices)
    for i in range(amount_wh):
        user_id = i % amount_users

        practice_id = i % amount_practices
        data = {
            "day_of_week": "Monday",
            "start_time": "10:00",
            "end_time": "14:00",
            "practice_id": str(practice_id),
        }
        client.post(
            url="/working_hours/create",
            content=json.dumps(data),
            headers=headers[user_id],
        )


def test_create_working_hours(client, normal_user_token_headers):
    # Test adding working hours
    data = {
        "day_of_week": "Monday",
        "start_time": "10:00",
        "end_time": "14:00",
        "practice_id": "1",
    }
    # Test adding working hours
    response = client.post(
        url="/working_hours/create",
        content=json.dumps(data),
        headers=normal_user_token_headers,
    )
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
def test_create_working_hours_wrong_fields(
    client, day_of_week, start_time, end_time, normal_user_token_headers
):
    # Test adding working hours
    data = {
        "day_of_week": day_of_week,
        "start_time": start_time,
        "end_time": end_time,
        "practice_id": 1,
    }
    response = client.post(
        url="/working_hours/create",
        content=json.dumps(data),
        headers=normal_user_token_headers,
    )
    assert response.status_code == 422


def test_retrieve_working_hours(client, normal_user_token_headers):
    add_working_hours(client)
    response = client.get("/working_hours/get/1")
    assert response.status_code == 200
    assert response.json()["day_of_week"] == "Monday"


def test_update_working_hours(client, normal_user_token_headers):
    add_working_hours(client)
    data = {
        "day_of_week": "Monday",
        "start_time": "10:00",
        "end_time": "21:37",
        "practice_id": 1,
    }

    response = client.put("/working_hours/update/1", content=json.dumps(data))
    assert response.json()["msg"] == "Successfully updated data."
    response = client.get("/working_hours/get/1")
    assert response.json()["end_time"] == "21:37"


def test_delete_working_hours(client, normal_user_token_headers):
    add_working_hours(client)
    response = client.delete("/working_hours/delete/1")
    assert response.json()["msg"] == "Successfully deleted data."
    response = client.get("/working_hours/get/1")
    assert response.status_code == 404


def test_get_doctors_working_hours(client, normal_user_token_headers):
    response = client.get("/working_hours/get_doctor/1")
    assert response.status_code == 200
    assert len(response.json()) == 0

    add_working_hours(
        client,
        amount_users=3,
        amount_practices=2,
        amount_wh=10,
    )
    response = client.get("/working_hours/get_doctor/2")
    assert response.status_code == 200
    assert response.json()[1]
