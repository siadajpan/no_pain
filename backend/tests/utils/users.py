from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.db.repository.users import create_new_user, get_user_by_email
from backend.schemas.users import UserCreate


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    user = get_user_by_email(email=email, db=db)
    if not user:
        user_in_create = UserCreate(
            email=email,
            password=settings.TEST_USER_PASSWORD,
        )
        user = create_new_user(user=user_in_create, db=db)

    headers = user_authentication_headers(
        client=client, email=email, password=settings.TEST_USER_PASSWORD
    )
    return headers
