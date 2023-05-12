from fastapi import APIRouter

from apis.v1 import route_general_pages, route_users, route_practice

api_router = APIRouter()
api_router.include_router(
    route_general_pages.general_pages_router, prefix="", tags=["general_pages"]
)
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(
    route_practice.router, prefix="/practices", tags=["practices"]
)
