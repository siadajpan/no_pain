from collections import defaultdict
from typing import Dict, List

from sqlalchemy.orm import Session

from backend.db.models.doctors import Doctor
from backend.db.models.practices import Practice
from backend.db.models.users import User
from backend.db.models.working_hours import WorkingHours
from backend.db.repository.users import create_new_user
from backend.schemas.doctors import DoctorCreate
from backend.schemas.users import UserCreate


def create_new_doctor(doctor: DoctorCreate, db: Session):
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


def get_doctor(doctor_id, db):
    return db.get(Doctor, doctor_id)


def list_all_doctors(db):
    doctors = db.query(Doctor).all()

    return doctors


def list_doctors_as_show_doctor(db):
    doctors_and_users = db.query(Doctor, User).join(User).all()
    if not len(doctors_and_users):
        return []

    # Show doctor expects an email
    for doctor, user in doctors_and_users:
        doctor.email = user.email
    return list(zip(*doctors_and_users))[0]


def get_doctors_working_hours_and_practices(doctor_id: int, db)\
        -> Dict[Practice, List[WorkingHours]]:
    doctors_working_hours_practices = (
        db.query(Practice, WorkingHours)
        .join(WorkingHours)
        .filter(WorkingHours.doctor_id == doctor_id)
        .all()
    )
    practice_groups = defaultdict(list)
    for practice, working_hours in doctors_working_hours_practices:
        practice_groups[practice].append(working_hours)

    return practice_groups

