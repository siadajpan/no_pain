from db.models.working_hours import WorkingHours
from schemas.working_hours import WorkingHoursCreate
from sqlalchemy.orm import Session


def create_new_working_hours(
    working_hours: WorkingHoursCreate, db: Session, user_id: int
):
    # TODO How to validate start and end time?
    # WorkingHoursCreate.validate_start_less_than_end(
    #     working_hours.start_time, working_hours.end_time
    # )
    new_working_hours = WorkingHours(
        user_id=user_id,
        **working_hours.dict(),
    )
    db.add(new_working_hours)
    db.commit()
    db.refresh(new_working_hours)

    return new_working_hours


def get_working_hours_by_id(working_hours_id: int, db: Session):
    hours = db.get(WorkingHours, working_hours_id)
    return hours or None


def update_working_hours_by_id(
    working_hours_id: int, working_hours: WorkingHoursCreate, db: Session
):
    existing_hours = db.get(WorkingHours, working_hours_id)
    if not existing_hours:
        return 0
    update_data = working_hours.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_hours, key, value)

    db.add(existing_hours)
    db.commit()
    db.refresh(existing_hours)
    return 1


def delete_working_hours_by_id(_id: int, db: Session):
    working_hours = db.get(WorkingHours, _id)
    if not working_hours:
        return 0

    db.delete(working_hours)
    db.commit()
    return 1


def get_working_hours_by_user_id(user_id: int, db: Session):
    all_hours = db.query(WorkingHours).all()
    print(f"All working hours: {[h.__dict__ for h in all_hours]}, {user_id}")
    users_working_hours = (
        db.query(WorkingHours).filter(WorkingHours.user_id == user_id).all()
    )
    print("User working hours", users_working_hours)
    return users_working_hours
