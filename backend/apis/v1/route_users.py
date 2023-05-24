from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.repository.users import create_new_user
from backend.db.session import get_db
from backend.schemas.users import ShowUser, UserCreate

router = APIRouter()


@router.post("/create", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
