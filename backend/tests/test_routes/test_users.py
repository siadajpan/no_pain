import json


def test_create_user(client):
    data = {
        "first_name": "name",
        "last_name": "last_name",
        "email": "testemail@email.com",
        "password": "testing",
    }
    response = client.post(url="/users/", content=json.dumps(data))
    assert response.status_code == 200
    assert response.json()["first_name"] == "name"
    assert response.json()["last_name"] == "last_name"
    assert response.json()["email"] == "testemail@email.com"
