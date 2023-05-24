from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.repository.doctors import create_new_doctor, list_doctors_as_show_doctor
from backend.db.session import get_db
from backend.schemas.doctors import DoctorCreate, ShowDoctor

router = APIRouter()


@router.post("/create", response_model=ShowDoctor)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    email = doctor.email
    new_doctor = create_new_doctor(doctor=doctor, db=db)
    # Needed for ShowDoctor class
    new_doctor.email = email

    return new_doctor


@router.get("/list", response_model=List[ShowDoctor])
def list_doctors(db: Session = Depends(get_db)):
    doctors = list_doctors_as_show_doctor(db)
    # for doctor in doctors:
    #     del doctor.hashed_password
    return doctors
