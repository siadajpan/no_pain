from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from no_pain.backend.db.base_class import Base


from no_pain.backend.db.models.associations import practice_patient

class Patient(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="patient")
    date_of_birth = Column(Date, nullable=True)

    practices = relationship("Practice", secondary=practice_patient, back_populates="patients")
