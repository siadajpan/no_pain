from fastapi import APIRouter, Depends, Request, responses
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from backend.db.models.doctors import DoctorSpeciality
from backend.db.repository.doctors import (
    create_new_doctor,
    get_doctor,
    get_doctors_working_hours_and_practices,
)
from backend.db.session import get_db
from backend.schemas.doctors import DoctorCreate
from backend.webapps.doctors.forms import DoctorCreateForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/details/{doctor_id}")
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


@router.get("/register/")
def register_form(request: Request):
    return templates.TemplateResponse(
        "doctors/register.html", {"request": request, "doctor_speciality": DoctorSpeciality}
    )


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = DoctorCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        new_doctor = DoctorCreate(
            first_name=form.first_name,
            last_name=form.last_name,
            email=form.email,
            password=form.password,
            speciality=DoctorSpeciality.DENTIST,  # TODO fix this to pass real type
        )
        try:
            create_new_doctor(doctor=new_doctor, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.errors.append("User with that e-mail already exists.")
            return templates.TemplateResponse("doctors/register.html", form.__dict__)
    return templates.TemplateResponse("doctors/register.html", form.__dict__)
