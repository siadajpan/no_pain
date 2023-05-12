from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Practice(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    street_number = Column(String, nullable=False)
    apartment_number = Column(Integer, nullable=True)
    working_hours = relationship("WorkingHours", back_populates="practice")
    # TODO Add city and unique name that is name+street+number+city