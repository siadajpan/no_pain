from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from no_pain.backend.db.base_class import Base


from no_pain.backend.db.models.associations import practice_doctor

class Doctor(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="doctor")
    specialization = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    
    practices = relationship("Practice", secondary=practice_doctor, back_populates="doctors")
