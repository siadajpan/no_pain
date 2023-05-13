from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    working_hours = relationship("WorkingHours", back_populates="user")
