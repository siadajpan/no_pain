from db.repository.practices import create_new_practice
from db.session import get_db
from fastapi import APIRouter, Depends
from schemas.practices import PracticeCreate, PracticeShow
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=PracticeShow)
def create_practice(practice: PracticeCreate, db: Session = Depends(get_db)):
    new_practice = create_new_practice(practice, db)
    return new_practice
