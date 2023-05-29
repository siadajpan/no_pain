import json

from fastapi import APIRouter, Depends, Request, responses
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
    get_doctors_working_hours_and_practices,
)
from backend.db.session import get_db
from backend.schemas.doctors import DoctorCreate
from backend.webapps.doctors.forms import DoctorCreateForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/details/{doctor_id}")
async def doctor_details(
    doctor_id: int, request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    doctors_working_hours_practices = get_doctors_working_hours_and_practices(
        doctor_id=doctor_id, db=db
    )
    doctor = get_doctor(doctor_id, db)
    current_user = get_current_user_from_token(token, db)
    editable: bool = current_user.id == doctor.user_id

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

#
# @router.post("/register/")
# async def add_working_hours(request: Request, db: Session = Depends(get_db)):
#     form = WorkingHoursCreateForm(request)
#     token = request.cookies.get("access_token")
#     scheme, param = get_authorization_scheme_param(
#                 token
#             )  # scheme will hold "Bearer" and param will hold actual token value
#     current_user: User = get_current_user_from_token(token=param, db=db)
#     if await form.is_valid():
#         for working_hours in form.working_hours:
#             create_new_working_hours(
#                 working_hours=working_hours, db=db, doctor_id=current_user.id
#             )
#
