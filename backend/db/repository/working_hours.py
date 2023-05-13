from db.models.working_hours import WorkingHours
from schemas.working_hours import WorkingHoursCreate
from sqlalchemy.orm import Session


def create_new_working_hours(
    working_hours: WorkingHoursCreate, db: Session, user_id: int, practice_id: int
):
    # TODO How to validate start and end time?
    # WorkingHoursCreate.validate_start_less_than_end(
    #     working_hours.start_time, working_hours.end_time
    # )
    new_working_hours = WorkingHours(
        **working_hours.dict(), user_id=user_id, practice_id=practice_id
    )
    db.add(new_working_hours)
    db.commit()
    db.refresh(new_working_hours)

    return new_working_hours
