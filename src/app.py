from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


static_files = StaticFiles(directory="src/static")
template_files = Jinja2Templates(directory='src/templates')


def get_app() -> FastAPI:
    from src.routers.auth import auth_router
    from src.routers.projects import projects_router
    from src.routers.issues import issues_router

    app = FastAPI()

    app.include_router(auth_router)
    app.include_router(projects_router)
    app.include_router(issues_router)

    app.mount("/static", static_files, name="static")

    return app
