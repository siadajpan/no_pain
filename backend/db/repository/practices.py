from db.models.practices import Practice
from schemas.practices import PracticeCreate
from sqlalchemy.orm import Session


def create_new_practice(practice: PracticeCreate, db: Session):
    new_practice = Practice(
        name=practice.name,
        postcode=practice.postcode,
        city=practice.city,
        street=practice.street,
        street_number=practice.street_number,
        apartment_number=practice.apartment_number,
        descriptor=f"{practice.name}.{practice.city}.{practice.street}.{practice.street_number}.{practice.apartment_number}",
    )
    db.add(new_practice)
    db.commit()
    db.refresh(new_practice)

    return new_practice
