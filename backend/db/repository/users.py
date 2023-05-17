from core.hashing import Hasher
from db.models.users import User
from fastapi import HTTPException
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from starlette import status


def create_new_user(user: UserCreate, db: Session):
    if get_user_by_email(user.email, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User creation failed. User with an email: {user.email}"
            f"already exists",
        )
    new_user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
