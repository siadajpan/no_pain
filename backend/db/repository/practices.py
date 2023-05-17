from http.client import HTTPException
from typing import List
from typing import Type

from db.models.practices import Practice
from db.repository.users import create_new_user
from db.repository.users import get_user_by_email
from schemas.practices import PracticeCreate
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from starlette import status


def create_new_practice(practice: PracticeCreate, db: Session):
    if get_user_by_email(practice.email, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creating practice failed. User with that email address "
            f"{practice.email} already exists",
        )
    create_new_user(UserCreate(email=practice.email, password=practice.password), db)

    del practice.email
    del practice.password

    new_practice = Practice(
        **practice.dict(),
        descriptor=f"{practice.name}.{practice.city}.{practice.street}.{practice.street_number}.{practice.apartment_number}",
    )
    db.add(new_practice)
    db.commit()
    db.refresh(new_practice)

    return new_practice


def retrieve_practice(practice_id: int, db: Session) -> Type[Practice]:
    item = db.get(Practice, practice_id)

    return item


def list_practices(db: Session) -> List[Type[Practice]]:
    practices = db.query(Practice).all()

    return practices
