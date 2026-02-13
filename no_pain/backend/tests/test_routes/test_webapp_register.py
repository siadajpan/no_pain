from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_register_page_loads(client: TestClient):
    response = client.get("/register/")
    assert response.status_code == 200
    assert "Register" in response.text

def test_register_new_user(client: TestClient, db_session: Session):
    # This test assumes the database is clean or email is unique
    user_data = {
        "email": "newuser@example.com",
        "nick": "News",
        "password": "strongpassword",
        "confirm_password": "strongpassword",
        "tos_agreement": "on"
    }
    response = client.post("/register/", data=user_data)
    
    # Expecting the verify notice page
    assert response.status_code == 200
    if "Confirm your email" not in response.text:
        print(response.text) # For debugging if it fails again
    assert "Confirm your email" in response.text
