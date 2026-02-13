from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from no_pain.backend.schemas.user import UserCreate
from no_pain.backend.webapps.base import api_router as web_app_router
from no_pain.backend.apis.base import api_router as backend_api_router
from no_pain.backend.core.config import settings
from no_pain.backend.db.base_class import Base
from no_pain.backend.db.session import get_db
from no_pain.backend.tests.utils.users import login_test_user

import no_pain.backend.db.base  # noqa - imports all the tables


def start_application():
    app = FastAPI()
    app.include_router(web_app_router)
    app.include_router(backend_api_router)
    from fastapi.staticfiles import StaticFiles
    from no_pain.backend.core.config import settings
    import os

    # Assuming static files are in no_pain/frontend/public relative to project root
    # __file__ is no_pain/backend/tests/conftest.py
    # dirname -> no_pain/backend/tests
    # dirname -> no_pain/backend
    # dirname -> no_pain
    # dirname -> root
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    static_dir = os.path.join(root_dir, "no_pain", "frontend", "public")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Creates a fresh database on each test case. This is where Base.metadata.create_all()
    must be called, after all models have been imported above.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    """
    Creates a new database session with a transaction that is rolled back after
    each test, ensuring isolation.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Creates a new FastAPI TestClient that overrides the `get_db` dependency
    to use the test database session.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def user_logged_in(client: TestClient, db_session: Session):
    """Logs in a test user for API testing."""
    login_test_user(client=client, email=settings.TEST_USER_EMAIL)


@pytest.fixture(scope="function")
def mock_user_create_data() -> UserCreate:
    """
    Provides a consistent UserCreate object for testing by instantiating
    the Pydantic model directly.
    """
    # Simply create and return an instance of the Pydantic model
    return UserCreate(
        email="test@example.com", password="securepassword123", nick="TestUserNick"
    )



