""" Auth Router
"""

from typing import Annotated

from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Query
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from src.core.app import template_files
from src.core.db import MongoDB
from src.core.db import DBCollectionsEnum


auth_router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@auth_router.post("/register")
async def register_post(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    """
    collection = await MongoDB.collection(DBCollectionsEnum.users)
    result = await collection.insert_one(
        {
            "username": form_data.username,
            "password": form_data.password,
        }
    )
    return str(result.inserted_id)
