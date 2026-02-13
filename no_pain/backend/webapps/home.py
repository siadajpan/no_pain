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

templates = Jinja2Templates(directory=TEMPLATES_DIR)
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_token),
    msg: str = None,
):
    # running_games = [g for t in user.teams for g in t.games if g.running]
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {
            "request": request,
            "msg": msg,
            "user": user,
            "running_games": [],
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
