from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from no_pain.backend.db.base_class import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=False)
    nick = Column(String(200), nullable=False)

    verification = relationship(
        "UserVerification", back_populates="user", uselist=False
    )
