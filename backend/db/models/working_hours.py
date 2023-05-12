from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class WorkingHours(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="working_hours")
    practice_id = Column(Integer, ForeignKey("practice.id"))
    practice = relationship("Practice", back_populates="working_hours")
