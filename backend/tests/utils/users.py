from core.config import settings
from db.repository.users import create_new_user
from db.repository.users import get_user_by_email
from fastapi.testclient import TestClient
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    print(f"posing for token with {data}")
    r = client.post("/login/token", data=data)
    print(f"Got response {r.json()}")
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    print("Getting user by email")
    user = get_user_by_email(email=email, db=db)
    print(f"Got user {user}")
    if not user:
        first_name = "First name"
        last_name = "Last name"
        user_in_create = UserCreate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=settings.TEST_USER_PASSWORD,
        )
        print(f"Created new user {user_in_create}")
        user = create_new_user(user=user_in_create, db=db)
        print(f"User after creation: {user.username} {user.email}")
    return user_authentication_headers(
        client=client, email=email, password=settings.TEST_USER_PASSWORD
    )
