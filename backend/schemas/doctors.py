from db.models.doctors import DoctorType
from pydantic import BaseModel
from pydantic import EmailStr


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
