import datetime
from typing import Annotated
from urllib.parse import urlparse
from urllib.parse import urlunparse

import pymongo
from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import status
from fastapi import Form
from fastapi import Query
from fastapi.responses import RedirectResponse

from src.core.app import template_files
from src.core.db import MongoDB
from src.core.db import DBCollectionsEnum
from src.core.enums import IssuesSupportedURLEnum
from src.routers.auth import get_current_user
from src.routers.auth import get_optional_current_user
from src.schemas.issues import IssuesModel


issues_router = APIRouter(prefix="/issues", tags=["issues"])


@issues_router.get("/", name="issues_get")
async def issues_get(
    request: Request,
    error_message: Annotated[
        str | None,
        Query(title="Error Message"),
    ] = None,
    current_user=Depends(get_optional_current_user),
):
    collection = await MongoDB.collection(DBCollectionsEnum.issues)
    db_issues = []

    async with collection.find().sort(
        "creation_dt", pymongo.DESCENDING,
    ) as cursor:
        async for issue in cursor:
            db_issues.append(IssuesModel(**issue))

    return template_files.TemplateResponse(
        request=request,
        name="issues/issues.html",
        context={
            "user": current_user,
            "issues": db_issues,
            "error_message": error_message,
        }
    )


@issues_router.get("/new", name="get_issues_new")
async def get_issues_new(
    request: Request,
    error_message: Annotated[
        str | None,
        Query(title="Error Message"),
    ] = None,
    current_user=Depends(get_current_user),
):
    return template_files.TemplateResponse(
        request=request,
        name="issues/issues_new.html",
        context={
            "user": current_user,
            "error_message": error_message,
        }
    )


@issues_router.post("/add", name="post_issues_add")
async def post_issues_add(
    url: Annotated[str, Form()],
    request: Request,
    current_user=Depends(get_current_user),
):
    parsed_url = urlparse(url)
    url_scheme = parsed_url.scheme
    url_netloc = parsed_url.netloc
    url_path = parsed_url.path

    if not all((url_scheme, url_netloc, url_path)):
        redirect_url = request.url_for(
            "issues_get"
        ).include_query_params(
            error_message="Issues Add Failed; Not valid URL.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_303_SEE_OTHER,
        )

    if url_netloc not in IssuesSupportedURLEnum:
        redirect_url = request.url_for(
            "issues_get"
        ).include_query_params(
            error_message="Issues Add Failed; URL is not supported.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_303_SEE_OTHER,
        )

    clean_url = urlunparse((url_scheme, url_netloc, url_path, '', '', ''))
    collection = await MongoDB.collection(DBCollectionsEnum.issues)
    db_issue = await collection.find_one({"url": clean_url})

    if db_issue:
        redirect_url = request.url_for(
            "issues_get"
        ).include_query_params(
            error_message=(
                f"Issues Add Failed; "
                f"URL exists (#{db_issue['_id']})."
            ),
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_302_FOUND,
        )

    await collection.insert_one(
        {
            "url": clean_url,
            "title": clean_url,
            "added_by": current_user["_id"],
            "creation_dt": str(datetime.datetime.now(tz=datetime.UTC)),
        }
    )

    return RedirectResponse(
        url=request.url_for("issues_get"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
