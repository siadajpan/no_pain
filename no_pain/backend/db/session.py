from typing import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from no_pain.backend.core.config import settings

# Dual database support: SQLite for local dev, PostgreSQL for production
USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

if USE_SQLITE:
    # SQLite configuration (for local development)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    print("Using SQLite database at ./sql_app.db")
else:
    # PostgreSQL configuration (for production)
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    print(f"Using PostgreSQL database at {settings.POSTGRES_SERVER}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

