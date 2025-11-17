from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.core.db import MongoDB
from src.exceptions.auth import InvalidCredentialsException


static_files = StaticFiles(directory="src/static")
template_files = Jinja2Templates(directory='src/templates')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.initialize()
    yield


async def exception_handler_ice(
    request: Request, exc: InvalidCredentialsException,
) -> Response:
    redirect_url = request.url_for(
        "get_login"
    ).include_query_params(
        error_message="Could not validate credentials.",
    )
    return RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


def get_app() -> FastAPI:
    from src.routers.auth import auth_router
    from src.routers.projects import projects_router
    from src.routers.issues import issues_router

    app = FastAPI(
        lifespan=lifespan,
        exception_handlers={
            InvalidCredentialsException: exception_handler_ice,
        }
    )

    app.include_router(auth_router)
    app.include_router(projects_router)
    app.include_router(issues_router)

    app.mount("/static", static_files, name="static")

    return app
