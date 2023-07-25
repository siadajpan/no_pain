import json
from typing import List

from fastapi import APIRouter, Depends, Request, responses, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from apis.v1.route_login import get_current_user_from_token, oauth2_scheme
from backend.db.models.doctors import DoctorSpeciality
from backend.db.repository.doctors import (
    create_new_doctor,
    get_doctor,
    get_doctors_working_hours_and_practices, list_doctors_as_show_doctor, get_doctor_by_user_id,
)
from backend.db.session import get_db
from backend.schemas.doctors import DoctorCreate, ShowDoctor
from backend.webapps.doctors.forms import DoctorCreateForm, WorkingHoursCreateForm
from backend.db.models.users import User
from db.repository.practices import retrieve_practice
from db.repository.working_hours import create_new_working_hours
from webapps.practices.route_practices import read_practices

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.post("/create", response_model=ShowDoctor)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    email = doctor.email
    new_doctor = create_new_doctor(doctor=doctor, db=db)
    # Needed for ShowDoctor class
    new_doctor.email = email

    return new_doctor


@router.get("/list", response_model=List[ShowDoctor])
def list_doctors(db: Session = Depends(get_db)):
    doctors = list_doctors_as_show_doctor(db)
    # for doctor in doctors:
    #     del doctor.hashed_password
    return doctors


@router.get("/details/{doctor_id}")
async def doctor_details(
        doctor_id: int, request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    doctors_working_hours_practices = get_doctors_working_hours_and_practices(
        doctor_id=doctor_id, db=db
    )
    doctor = get_doctor(doctor_id, db)
    if token:
        current_user = get_current_user_from_token(token, db)
        editable: bool = current_user.id == doctor.user_id
    else:
        editable = False

    return templates.TemplateResponse(
        "doctors/details.html",
        {
            "request": request,
            "doctor": doctor,
            "working_hours_practices": doctors_working_hours_practices,
            "editable": editable
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
        try:
            new_doctor = DoctorCreate(
                first_name=form.first_name,
                last_name=form.last_name,
                email=form.email,
                password=form.password,
                speciality=DoctorSpeciality.DENTIST,  # TODO fix this to pass real type
            )
        except ValidationError as e:
            for error in json.loads(e.json()):
                error = f"There is are some problems with {error['loc'][0]}"
                form.errors.append(error)
            return templates.TemplateResponse("doctors/register.html", form.__dict__)
        try:
            create_new_doctor(doctor=new_doctor, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.errors.append("User with that e-mail already exists.")
            return templates.TemplateResponse("doctors/register.html", form.__dict__)
    return templates.TemplateResponse("doctors/register.html", form.__dict__)


@router.get("/add_working_hours/")
def add_working_hours_form(request: Request, db: Session = Depends(get_db)):
    practices = read_practices(db)
    return templates.TemplateResponse(
        "doctors/add_working_hours.html", {"request": request, "practices": practices}
    )


@router.get("/add_working_hours_practice/{practice_id}")
def register_form(practice_id, request: Request, db: Session = Depends(get_db)):
    print("retrieving practice")
    practice = retrieve_practice(practice_id=practice_id, db=db)
    return templates.TemplateResponse(
        "doctors/add_working_hours_practice.html", {"request": request, "practice": practice}
    )


@router.post("/add_working_hours_practice/{practice_id}")
async def add_working_hours(practice_id, request: Request, db: Session = Depends(get_db)):
    form = WorkingHoursCreateForm(request)
    await form.load_data(practice_id)
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
        token
    )  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    current_doctor = get_doctor_by_user_id(current_user.id, db)

    if await form.is_valid():
        # print("form valid", form.working_hours["monday"].start, form.working_hours["monday"].end)

        for working_hours in form.working_hours:
            working_hours.practice_id = practice_id
            create_new_working_hours(
                working_hours=working_hours, db=db, doctor_id=current_doctor.id
            )
        return responses.RedirectResponse(
            "/?msg=Successfully added working hours", status_code=status.HTTP_302_FOUND
        )  # default is post request, to use get request added status code 302
    return templates.TemplateResponse("doctors/add_working_hours.html", form.__dict__)
