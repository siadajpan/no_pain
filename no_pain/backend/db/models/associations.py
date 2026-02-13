from sqlalchemy import Column, ForeignKey, Integer, Table
from no_pain.backend.db.base_class import Base

practice_doctor = Table(
    "practice_doctor",
    Base.metadata,
    Column("practice_id", Integer, ForeignKey("practice.id"), primary_key=True),
    Column("doctor_id", Integer, ForeignKey("doctor.id"), primary_key=True),
)

practice_patient = Table(
    "practice_patient",
    Base.metadata,
    Column("practice_id", Integer, ForeignKey("practice.id"), primary_key=True),
    Column("patient_id", Integer, ForeignKey("patient.id"), primary_key=True),
)
