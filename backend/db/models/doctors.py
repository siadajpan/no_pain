import enum

from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class DoctorType(enum.Enum):
    DENTIST = "dentist"


class Doctor(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="doctor")
    doctor_type = Column(Enum(DoctorType), nullable=False)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    working_hours = relationship("WorkingHours", back_populates="doctor")
