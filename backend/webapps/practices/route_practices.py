from db.repository.practices import create_new_practice
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi.templating import Jinja2Templates
from schemas.practices import PracticeCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from webapps.practices.forms import PracticeCreateForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/details/{practice_id}")
async def practice_details(
    doctor_id: int, request: Request, db: Session = Depends(get_db)
):
    pass
    # doctors_working_hours_practices = get_doctors_working_hours_and_practices(
    #     doctor_id=doctor_id, db=db
    # )
    # practice = get_practice(doctor_id, db)
    # return templates.TemplateResponse(
    #     "doctors/details.html",
    #     {
    #         "request": request,
    #         "doctor": practice,
    #         "working_hours_practices": doctors_working_hours_practices,
    #     },
    # )


@router.get("/register/")
def register_form(request: Request):
    return templates.TemplateResponse("practices/register.html", {"request": request})


@router.post("/register/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = PracticeCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        new_practice = PracticeCreate(
            name=form.name,
            email=form.email,
            password=form.password,
            address=form.address,
            postcode=form.postcode,
            city=form.city,
        )
        try:
            create_new_practice(practice=new_practice, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.errors.append("User with that e-mail already exists.")
            return templates.TemplateResponse("practices/register.html", form.__dict__)
    return templates.TemplateResponse("practices/register.html", form.__dict__)
