import json

from db.models.users import User


def test_create_user(client):
    data = {
        "first_name": "name",
        "last_name": "last_name",
        "email": "testemail@email.com",
        "password": "testing",
    }
    response = client.post(url="/users/create", content=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["first_name"] == "name"
    assert response.json()["last_name"] == "last_name"
    assert response.json()["email"] == "testemail@email.com"



def test_adding_same_user_twice(client):
    user = {
        "first_name": "name",
        "last_name": "last_name",
        "email": "testemail@email.com",
        "password": "testing",
    }
    response = client.post(url="/users/create", content=json.dumps(user))
    assert response.json()["username"] == "name.last_name"
    user2 = user.copy()
    user2["email"] = "testemail2@email.com"
    response = client.post(url="/users/create", content=json.dumps(user2))
    assert response.status_code == 200
    assert response.json()["username"] == "name.last_name.1"
