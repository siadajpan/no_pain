from apis.v1 import (
    route_general_pages,
    route_practice,
    route_users,
    route_working_hours,
)
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(
    route_general_pages.general_pages_router, prefix="", tags=["general_pages"]
)
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(
    route_practice.router, prefix="/practices", tags=["practices"]
)
api_router.include_router(
    route_working_hours.router, prefix="/working_hours", tags=["working_hours"]
)
