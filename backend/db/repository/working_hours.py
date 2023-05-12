from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from db.models.working_hours import WorkingHours
from db.session import get_db
from schemas.working_hours import WorkingHoursCreate, WorkingHoursShow

def create_new_working_hours(
        working_hours: WorkingHoursCreate,
        db: Session
):
    new_working_hours = WorkingHours(
        user_id=working_hours.user_id,
        practice_id=working_hours.practice_id,
        day_of_week=working_hours.day_of_week,
        start_time=working_hours.start_time,
        end_time=working_hours.end_time,
    )
    db.add(new_working_hours)
    db.commit()
    db.refresh(new_working_hours)

    return new_working_hours