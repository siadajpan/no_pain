from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    working_hours = relationship("WorkingHours", back_populates="user")
