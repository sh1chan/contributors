""" Auth Router
"""

from typing import Annotated

from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Query
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from pwdlib import PasswordHash

from src.core.app import template_files
from src.core.db import MongoDB
from src.core.db import DBCollectionsEnum


auth_router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return password_hash.hash(plain_password)


@auth_router.get("/register", name="register_get")
async def register_get(
    request: Request,
    error_message: Annotated[
        str | None,
        Query(title="Error Message"),
    ] = None,
):
    return template_files.TemplateResponse(
        request=request,
        name="auth/register.html",
        context={
            "error_message": error_message,
        }
    )


@auth_router.post("/register", name="register_post")
async def register_post(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    """
    username = form_data.username.strip()
    password = form_data.password.strip()

    if not all((username, password)):
        redirect_url = request.url_for(
            "register_get"
        ).include_query_params(
            error_message="Register Failed; Credentials are required.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_302_FOUND,
        )

    collection = await MongoDB.collection(DBCollectionsEnum.users)
    db_user = await collection.find_one({"username": username})

    if db_user:
        redirect_url = request.url_for(
            "register_get"
        ).include_query_params(
            error_message="Register Failed; Username must be unique.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_302_FOUND,
        )

    await collection.insert_one(
        {
            "username": username,
            "password": get_password_hash(password),
        }
    )

    return RedirectResponse(
        url=request.url_for("login_get"),
        status_code=status.HTTP_302_FOUND,
    )


@auth_router.get("/login", name="login_get")
async def login_get(
    request: Request,
    error_message: Annotated[
        str | None,
        Query(title="Error Message"),
    ] = None,
):
    return template_files.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={
            "error_message": error_message,
        }
    )
