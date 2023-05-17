from apis.v1 import route_doctors
from apis.v1 import route_general_pages
from apis.v1 import route_login
from apis.v1 import route_practice
from apis.v1 import route_users
from apis.v1 import route_working_hours
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(
    route_general_pages.general_pages_router, prefix="", tags=["general_pages"]
)
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_doctors.router, prefix="/doctors", tags=["doctors"])
api_router.include_router(
    route_practice.router, prefix="/practices", tags=["practices"]
)
api_router.include_router(
    route_working_hours.router, prefix="/working_hours", tags=["working_hours"]
)
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
