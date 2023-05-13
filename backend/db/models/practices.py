from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Practice(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    street_number = Column(String, nullable=False)
    apartment_number = Column(String, nullable=True)
    working_hours = relationship("WorkingHours", back_populates="practice")
    descriptor = Column(String, unique=True, nullable=False)
