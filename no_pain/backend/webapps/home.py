from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from no_pain.backend.apis.v1.route_login import (
    get_current_user_from_token,
)
from no_pain.backend.core.config import TEMPLATES_DIR
from no_pain.backend.db.models.user import User
from no_pain.backend.db.session import get_db
from no_pain.backend.db.models.user_role import UserRole
from no_pain.backend.db.repository.doctor import list_doctors, get_doctor_by_slug
from no_pain.backend.db.repository.practice import list_practices, get_practice_by_slug

templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
    msg: str = None,
):
    doctors = []
    practices = []
    my_doctors = []
    my_practices = []
    all_doctors_json = []
    all_practices_json = []

    if user and user.role == UserRole.PATIENT:
        doctors = list_doctors(db)
        practices = list_practices(db)
    elif user and user.role == UserRole.PRACTICE and user.practice:
        # Eager load doctors for this practice
        db.refresh(user.practice, ["doctors"])
        my_doctors = user.practice.doctors
        # Build JSON list of all doctors for search
        all_docs = list_doctors(db)
        existing_ids = {d.id for d in my_doctors}
        all_doctors_json = [
            {"id": d.id, "first_name": d.user.first_name, "last_name": d.user.last_name,
             "specialization": d.specialization or "", "name": f"{d.user.first_name} {d.user.last_name}"}
            for d in all_docs if d.id not in existing_ids
        ]
    elif user and user.role == UserRole.DOCTOR and user.doctor:
        # Eager load practices for this doctor
        db.refresh(user.doctor, ["practices"])
        my_practices = user.doctor.practices
        # Build JSON list of all practices for search
        all_pracs = list_practices(db)
        existing_ids = {p.id for p in my_practices}
        all_practices_json = [
            {"id": p.id, "name": p.name or "", "city": p.city or ""}
            for p in all_pracs if p.id not in existing_ids
        ]

    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {
            "request": request,
            "msg": msg,
            "user": user,
            "doctors": doctors,
            "practices": practices,
            "my_doctors": my_doctors,
            "my_practices": my_practices,
            "all_doctors_json": all_doctors_json,
            "all_practices_json": all_practices_json,
            "UserRole": UserRole,
        },
    )


@router.get("/terms-of-service/")
async def terms_of_service(request: Request):
    return templates.TemplateResponse(
        "general_pages/terms_of_service.html", {"request": request}
    )


@router.get("/privacy-policy/")
async def privacy_policy(request: Request):
    return templates.TemplateResponse(
        "general_pages/privacy_policy.html", {"request": request}
    )


@router.get("/{slug}")
async def view_profile(slug: str, request: Request, db: Session = Depends(get_db)):
    # Try finding a doctor
    doctor = get_doctor_by_slug(slug, db)
    if doctor:
        return templates.TemplateResponse(
            "general_pages/doctor_profile.html", {"request": request, "doctor": doctor}
        )
    
    # Try finding a practice
    practice = get_practice_by_slug(slug, db)
    if practice:
        return templates.TemplateResponse(
            "general_pages/practice_profile.html", {"request": request, "practice": practice}
        )

    # 404 if not found (or maybe just return 404 template)
    return templates.TemplateResponse(
        "general_pages/404.html", {"request": request}, status_code=404
    )
