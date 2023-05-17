from fastapi import APIRouter
from webapps.doctors import route_doctors


api_router = APIRouter()
api_router.include_router(route_doctors.router, prefix="", tags=["doctors-webapp"])
