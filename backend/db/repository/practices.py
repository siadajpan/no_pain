from typing import List
from typing import Type

from db.models.practices import Practice
from schemas.practices import PracticeCreate
from sqlalchemy.orm import Session


def create_new_practice(practice: PracticeCreate, db: Session):
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
