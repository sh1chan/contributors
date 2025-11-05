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
from src.schemas.issues import IssuesNewIn


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


@issues_router.post("/new", name="post_issues_new")
async def post_issues_new(
    form_data: Annotated[IssuesNewIn, Form()],
    request: Request,
    current_user=Depends(get_current_user),
):
    collection = await MongoDB.collection(DBCollectionsEnum.issues)

    if form_data.url:
        parsed_url = urlparse(form_data.url)
        url_scheme = parsed_url.scheme
        url_netloc = parsed_url.netloc
        url_path = parsed_url.path

        if not all((url_scheme, url_netloc, url_path)):
            redirect_url = request.url_for(
                "get_issues_new"
            ).include_query_params(
                error_message="Issues New Failed; Not valid URL.",
            )
            return RedirectResponse(
                url=redirect_url,
                status_code=status.HTTP_303_SEE_OTHER,
            )

        if url_netloc not in IssuesSupportedURLEnum:
            redirect_url = request.url_for(
                "get_issues_new"
            ).include_query_params(
                error_message="Issues New Failed; URL is not supported.",
            )
            return RedirectResponse(
                url=redirect_url,
                status_code=status.HTTP_303_SEE_OTHER,
            )

        form_data.url = urlunparse((
            url_scheme, url_netloc, url_path, '', '', '',
        ))
        db_issue = await collection.find_one({"url": form_data.url})

        if db_issue:
            redirect_url = request.url_for(
                "get_issues_new"
            ).include_query_params(
                error_message=(
                    f"Issues New Failed; "
                    f"URL exists (#{db_issue['_id']})."
                ),
            )
            return RedirectResponse(
                url=redirect_url,
                status_code=status.HTTP_302_FOUND,
            )

    document = {
        "url": form_data.url,
        "title": form_data.title,
        "description": form_data.description,
        "tags": form_data.all_tags,
        "labels": form_data.all_labels,
        "creation_dt": str(datetime.datetime.now(tz=datetime.UTC)),
    }
    if form_data.url:
        document["added_by"] = current_user["_id"]
    else:
        document["created_by"] = current_user["_id"]

    result = await collection.insert_one(document=document)

    redirect_url = request.url_for(
        "get_issues_new"
    ).include_query_params(
        error_message=f"Issues New Succeed; (#{result.inserted_id})",
    )
    return RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_303_SEE_OTHER,
    )
