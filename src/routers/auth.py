""" Auth Router
"""

from fastapi import APIRouter
from fastapi import Request

from src.app import template_files


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/register")
async def register_get(request: Request):
    return template_files.TemplateResponse(
        request=request,
        name="auth/register.html",
    )


@auth_router.post("/register")
async def register_post():
    return {}
