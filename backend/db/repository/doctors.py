from db.models.doctors import Doctor
from db.models.practices import Practice
from db.models.users import User
from db.models.working_hours import WorkingHours
from db.repository.users import create_new_user
from schemas.doctors import DoctorCreate
from schemas.users import UserCreate
from sqlalchemy.orm import Session


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


def get_doctors_working_hours_and_practices(doctor_id: int, db, group_by_practice=True):
    doctors_working_hours_practices = (
        db.query(Practice, WorkingHours)
        .join(WorkingHours)
        .filter(WorkingHours.doctor_id == doctor_id)
        .all()
    )

    print("User working hours", [d for d in doctors_working_hours_practices])
    return doctors_working_hours_practices
