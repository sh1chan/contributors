from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from src.core.app import template_files
from src.routers.auth import get_optional_current_user


issues_router = APIRouter(prefix="/issues", tags=["issues"])


@issues_router.get("/", name="issues_get")
async def issues_get(
    request: Request,
    current_user=Depends(get_optional_current_user),
):
    return template_files.TemplateResponse(
        request=request,
        name="issues/issues.html",
        context={
            "user": current_user,
            "issues": [],
        }
    )
