from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.users import User
from schemas.users import UserCreate


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=f"{user.first_name}.{user.last_name}",
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
