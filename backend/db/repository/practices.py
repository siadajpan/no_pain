from sqlalchemy.orm import Session

from db.models.practices import Practice
from schemas.practices import PracticeCreate


def create_new_practice(practice: PracticeCreate, db: Session):
    new_practice = Practice(
        name=practice.name,
        street=practice.street,
        street_number=practice.street_number,
        apartment_number=practice.apartment_number,
    )
    db.add(new_practice)
    db.commit()
    db.refresh(new_practice)

    return new_practice
