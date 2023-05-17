from db.models.doctors import Doctor
from db.models.users import User
from db.repository.users import create_new_user
from db.repository.users import get_user_by_email
from fastapi import HTTPException
from schemas.doctors import DoctorCreate
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from starlette import status


def create_new_doctor(doctor: DoctorCreate, db: Session):
    if get_user_by_email(doctor.email, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creating doctor failed. User with that email address "
            f"{doctor.email} already exists",
        )
    new_user = create_new_user(
        UserCreate(email=doctor.email, password=doctor.password), db
    )

    del doctor.email
    del doctor.password

    new_doctor = Doctor(user_id=new_user.id, **doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


def list_all_doctors(db):
    doctors = db.query(Doctor).all()

    return doctors


def list_doctors_as_show_doctor(db):
    doctors_and_users = (
        db.query(Doctor, User).join(User, User.id == Doctor.user_id).all()
    )
    if not len(doctors_and_users):
        return []

    # Show doctor expects an email
    for doctor, user in doctors_and_users:
        doctor.email = user.email
    return list(zip(*doctors_and_users))[0]
