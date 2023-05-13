from core.hashing import Hasher
from db.models.users import User
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    same_name_users = (
        db.query(User)
        .filter(User.first_name == user.first_name and User.last_name == user.last_name)
        .all()
    )
    suffix = f".{len(same_name_users)}" if len(same_name_users) else ""
    new_user = User(
        username=f"{user.first_name}.{user.last_name}{suffix}",
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
