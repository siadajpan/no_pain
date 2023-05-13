from http.client import HTTPException

from db.repository.practices import create_new_practice
from db.repository.practices import retrieve_practice
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from schemas.practices import PracticeCreate
from schemas.practices import PracticeShow
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()


@router.post("/create", response_model=PracticeShow)
def create_practice(practice: PracticeCreate, db: Session = Depends(get_db)):
    new_practice = create_new_practice(practice, db)
    return new_practice


@router.get("/get/{practice_id}")
def read_practice(practice_id: int, db: Session = Depends(get_db)):
    practice = retrieve_practice(practice_id=practice_id, db=db)
    if not practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practice with that id {id} doesn't exist",
        )
    return practice
