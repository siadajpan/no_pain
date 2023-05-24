from pydantic import BaseModel, EmailStr

from backend.db.models.doctors import DoctorType


class DoctorCreate(BaseModel):
    email: EmailStr
    password: str
    doctor_type: DoctorType
    first_name: str
    last_name: str


class ShowDoctor(BaseModel):
    id: str
    user_id: str
    email: str
    first_name: str
    last_name: str
    doctor_type: DoctorType

    class Config:
        orm_mode = True
