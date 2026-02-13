from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from no_pain.backend.db.base_class import Base


from no_pain.backend.db.models.associations import practice_doctor, practice_patient

class Practice(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="practice")
    name = Column(String, nullable=True)
    street_address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    doctors = relationship("Doctor", secondary=practice_doctor, back_populates="practices")
    patients = relationship("Patient", secondary=practice_patient, back_populates="practices")
