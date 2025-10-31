""" Auth Router
"""

import datetime
from typing import Annotated

import jwt
from pwdlib import PasswordHash
from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Query
from fastapi import Cookie
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from src.core.app import template_files
from src.core.db import MongoDB
from src.core.db import DBCollectionsEnum
from src.core.config import Secret
from src.core.enums import CookiesKeysEnum
from src.schemas.auth import TokenData


auth_router = APIRouter(prefix="/auth", tags=["auth"])

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return password_hash.hash(plain_password)


def create_access_token(data: dict, expires_delta: datetime.timedelta):
    """
    """
    return jwt.encode(
        {
            **data,
            "exp": datetime.datetime.now(
                datetime.timezone.utc
            ) + expires_delta,
        },
        Secret.SECRET_KEY,
        algorithm=Secret.ALGORITHM,
    )


async def get_optional_current_user(
    access_token: Annotated[str | None, Cookie()] = None,
):
    if not access_token:
        return None

    try:
        payload = jwt.decode(
            access_token,
            key=Secret.SECRET_KEY,
            algorithms=[Secret.ALGORITHM],
        )
    except jwt.exceptions.InvalidTokenError:
        return None

    username = payload.get("sub")

    if username is None:
        return None

    collection = await MongoDB.collection(DBCollectionsEnum.users)
    db_user = await collection.find_one({"username": username})

    if db_user is None:
        return None

    return db_user


async def get_current_user(
    access_token: Annotated[str | None, Cookie()] = None,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        raise credentials_exception
    try:
        payload = jwt.decode(
            access_token,
            key=Secret.SECRET_KEY,
            algorithms=[Secret.ALGORITHM],
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception

    collection = await MongoDB.collection(DBCollectionsEnum.users)
    db_user = await collection.find_one({"username": token_data.username})
    if db_user is None:
        raise credentials_exception

    return db_user


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


@auth_router.post("/login", name="login_post")
async def login_post(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    """
    redirect_url = request.url_for(
        "login_get"
    ).include_query_params(
        error_message="Login Failed; Invalid credentials.",
    )

    username = form_data.username.strip()
    password = form_data.password.strip()

    if not all((username, password)):
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_302_FOUND,
        )

    collection = await MongoDB.collection(DBCollectionsEnum.users)
    db_user = await collection.find_one({"username": username})

    if not db_user:
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_302_FOUND,
        )

    if not verify_password(password, db_user["password"]):
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_302_FOUND,
        )

    access_token = create_access_token(
        data={"sub": db_user["username"]},
        expires_delta=datetime.timedelta(
            minutes=Secret.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
    )

    response = RedirectResponse(
        url=request.url_for("issues_get"),
        status_code=status.HTTP_302_FOUND,
    )
    response.set_cookie(CookiesKeysEnum.access_token, access_token)

    return response


@auth_router.get("/logout", name="logout_get")
async def logout_get(
    request: Request,
    _=Depends(get_current_user)
):
    response = RedirectResponse(
        url=request.url_for("issues_get"),
        status_code=status.HTTP_302_FOUND,
    )
    response.delete_cookie(CookiesKeysEnum.access_token)

    return response
