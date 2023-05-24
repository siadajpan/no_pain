from fastapi import APIRouter

from backend.apis.v1 import (
    route_doctors,
    route_login,
    route_practice,
    route_users,
    route_working_hours,
)

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_doctors.router, prefix="/doctors", tags=["doctors"])
api_router.include_router(
    route_practice.router, prefix="/practices", tags=["practices"]
)
api_router.include_router(
    route_working_hours.router, prefix="/working_hours", tags=["working_hours"]
)
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
