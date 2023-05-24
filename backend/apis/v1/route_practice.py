from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.db.repository.practices import (
    create_new_practice,
    list_practices,
    retrieve_practice,
)
from backend.db.session import get_db
from backend.schemas.practices import PracticeCreate, PracticeShow

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


@router.get("/all", response_model=List[PracticeShow])
def read_practices(db: Session = Depends(get_db)):
    practices = list_practices(db=db)

    return practices
