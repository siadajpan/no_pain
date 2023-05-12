from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine


def include_router(app):
    app.include_router(api_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()

# @app.get("/") #remove this, It is no longer needed.
# def hello_api():
#     return {"msg":"Hello API"}
