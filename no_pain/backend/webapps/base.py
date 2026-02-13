from fastapi import APIRouter

from no_pain.backend.apis.v1 import route_health, route_login
from no_pain.backend.webapps import home
from no_pain.backend.webapps.auth import route_user_login

from no_pain.backend.webapps.user import route_user
from no_pain.backend.webapps.auth import route_verify
from no_pain.backend.webapps import route_association

api_router = APIRouter()
api_router.include_router(route_user.router, prefix="/user", tags=["user-webapp"])
api_router.include_router(route_health.health_router, prefix="")

api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
api_router.include_router(route_user_login.router, prefix="", tags=["auth-webapp"])
api_router.include_router(route_verify.router, prefix="", tags=["auth-webapp"])
api_router.include_router(route_association.router, prefix="", tags=["association-webapp"])

# home.router MUST be last because it has a /{slug} catch-all route
api_router.include_router(home.router, prefix="", tags=["user-webapp"])
