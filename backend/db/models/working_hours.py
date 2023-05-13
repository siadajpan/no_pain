from db.base_class import Base
from schemas.types import DayOfWeek
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class WorkingHours(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="working_hours")
    practice_id = Column(Integer, ForeignKey("practice.id"))
    practice = relationship("Practice", back_populates="working_hours")
    day_of_week = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
