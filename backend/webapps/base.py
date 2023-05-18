from fastapi import APIRouter
from webapps import home
from webapps.doctors import route_doctors
from webapps.practices import route_practices

api_router = APIRouter()
api_router.include_router(
    route_doctors.router, prefix="/doctors", tags=["doctors-webapp"]
)
api_router.include_router(home.router, prefix="", tags=["doctors-webapp"])
api_router.include_router(
    route_practices.router, prefix="/practices", tags=["practices-webapp"]
)
