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
    
    if user and user.role == UserRole.PATIENT:
        doctors = list_doctors(db)
        practices = list_practices(db)

    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {
            "request": request,
            "msg": msg,
            "user": user,
            "doctors": doctors,
            "practices": practices,
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
