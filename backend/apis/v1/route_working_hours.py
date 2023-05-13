from db.repository.working_hours import create_new_working_hours
from db.repository.working_hours import delete_working_hours_by_id
from db.repository.working_hours import get_working_hours_by_id
from db.repository.working_hours import update_working_hours_by_id
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from schemas.working_hours import WorkingHoursCreate
from schemas.working_hours import WorkingHoursShow
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()


@router.post("/create", response_model=WorkingHoursShow)
def create_working_hours(
    working_hours: WorkingHoursCreate, db: Session = Depends(get_db)
):
    current_user = 1
    practice_id = 1
    new_working_hours = create_new_working_hours(
        working_hours=working_hours,
        db=db,
        user_id=current_user,
        practice_id=practice_id,
    )

    return new_working_hours


@router.get("/get/{working_hours_id}", response_model=WorkingHoursShow)
def get_working_hours(working_hours_id, db: Session = Depends(get_db)):
    working_hours = get_working_hours_by_id(working_hours_id, db)
    if not working_hours:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Getting working hours failed. Element with id "
            f"{working_hours_id} not found",
        )
    return working_hours


@router.put("/update/{working_hours_id}")
def update_working_hours(
    working_hours_id,
    working_hours_update: WorkingHoursCreate,
    db: Session = Depends(get_db),
):
    response = update_working_hours_by_id(working_hours_id, working_hours_update, db)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Update working hours failed. Element with id "
            f"{working_hours_id} not found",
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{_id}")
def delete_working_hours(_id, db: Session = Depends(get_db)):
    response = delete_working_hours_by_id(_id=_id, db=db)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deleting working hours failed. Element with id "
            f"{_id} not found",
        )
    return {"msg": "Successfully deleted data."}
