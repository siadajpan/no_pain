from db.repository.working_hours import create_new_working_hours
from db.session import get_db
from fastapi import APIRouter, Depends
from schemas.working_hours import WorkingHoursCreate, WorkingHoursShow
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=WorkingHoursShow)
def create_working_hours(
    working_hours: WorkingHoursCreate, db: Session = Depends(get_db)
):
    new_working_hours = create_new_working_hours(working_hours=working_hours, db=db)

    return new_working_hours
