import json

import pytest
from sqlalchemy.exc import IntegrityError

from backend.db.models.doctor_type import DoctorType


def create_test_doctors(client, amount=1):
    doctors = []
    for i in range(amount):
        data = {
            "email": f"testemail{i}@email.com",
            "password": "testing",
            "doctor_type": DoctorType.DENTIST.value,
            "first_name": "Test name",
            "last_name": "Test last name",
        }
        response = client.post(url="/doctors/create", content=json.dumps(data))
        doctor_created = response.json()
        doctor_created.update({"password": "testing"})
        doctors.append(doctor_created)
    return doctors


def test_create_doctor(client):
    data = {
        "email": "testemail@email.com",
        "password": "testing",
        "doctor_type": DoctorType.DENTIST.value,
        "first_name": "Test name",
        "last_name": "Test last name",
    }
    response = client.post(url="/doctors/create", content=json.dumps(data))
    print(response.json())
    assert response.status_code == 200
    assert response.json()["first_name"] == "Test name"
    assert response.json()["doctor_type"] == DoctorType.DENTIST.value
    assert response.json()["id"] is not None
    assert response.json()["user_id"] is not None


def test_adding_same_doctor_twice(client):
    user = {
        "email": "testemail@email.com",
        "password": "testing",
        "doctor_type": DoctorType.DENTIST.value,
        "first_name": "Test name",
        "last_name": "Test last name",
    }
    response = client.post(url="/doctors/create", content=json.dumps(user))
    assert response.status_code == 200
    assert response.json()["first_name"] == "Test name"
    user2 = user.copy()
    with pytest.raises(IntegrityError):
        response = client.post(url="/doctors/create", content=json.dumps(user2))
    # assert response.status_code == 404


def test_list_doctors(client):
    create_test_doctors(client, 3)
    response = client.get(url="/doctors/list")
    assert response.status_code == 200
    assert len(response.json()) == 3
