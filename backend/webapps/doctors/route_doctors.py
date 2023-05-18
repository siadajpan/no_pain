from db.repository.doctors import get_doctor
from db.repository.doctors import get_doctors_working_hours_and_practices
from db.repository.doctors import list_doctors_as_show_doctor
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    doctors = list_doctors_as_show_doctor(db=db)

    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "doctors": doctors}
    )


@router.get("/doctors/details/{doctor_id}")
async def doctor_details(
    doctor_id: int, request: Request, db: Session = Depends(get_db)
):
    doctors_working_hours_practices = get_doctors_working_hours_and_practices(
        doctor_id=doctor_id, db=db
    )
    doctor = get_doctor(doctor_id, db)
    return templates.TemplateResponse(
        "doctors/details.html",
        {
            "request": request,
            "doctor": doctor,
            "working_hours_practices": doctors_working_hours_practices,
        },
    )
