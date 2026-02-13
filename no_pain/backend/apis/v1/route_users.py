from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from no_pain.backend.db.repository.user import create_new_user, get_user_by_email
from no_pain.backend.db.session import get_db
from no_pain.backend.schemas.user import UserCreate

router = APIRouter()


@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/get/{email}")
def get_user(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(email, db)
    return user
