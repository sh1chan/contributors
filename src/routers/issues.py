import datetime
from typing import Annotated
from urllib.parse import urlparse
from urllib.parse import urlunparse

import pymongo
from bson import ObjectId
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
from src.core.enums import CCategoriesIdentifiersEnum
from src.core.enums import IssuesSupportedURLEnum
from src.core.enums import CookiesKeysEnum
from src.routers.auth import get_current_user
from src.routers.auth import get_optional_current_user
from src.schemas.issues import IssuesModel
from src.schemas.issues import IssuesNewIn
from src.schemas.issues import IssuesFiltersModel


issues_router = APIRouter(prefix="/issues", tags=["issues"])


@issues_router.post("/", name="post_issues")
async def post_issues(
    form_data: Annotated[IssuesFiltersModel, Form()],
    request: Request,
):
    """ Saves filters in the cookies
    """
    response = RedirectResponse(
        url=request.url_for("issues_get"),
        status_code=status.HTTP_302_FOUND,
    )
    response.set_cookie(CookiesKeysEnum.filters, form_data.model_dump_json())

    return response


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
    query = {}

    filters = request.cookies.get(CookiesKeysEnum.filters)
    if filters:
        filters = IssuesFiltersModel.model_validate_json(filters)
        if filters.title:
            query["$text"] = {'$search': filters.title}
        if filters.tags:
            query["categories.tags"] = {'$in': filters.all_tags}
        if filters.labels:
            query["categories.labels"] = {'$in': filters.all_labels}
        if filters.id:
            query["_id"] = ObjectId(filters.id)
        if filters.created_by:
            query["created_by"] = ObjectId(filters.created_by)

    async with collection.find(query).sort(
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
            "filters": filters,
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
    categories_collection = await MongoDB.collection(
        DBCollectionsEnum.categories,
    )

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

    categories = {
        "tags": form_data.all_tags,
        "labels": form_data.all_labels,
    }

    result = await collection.insert_one({
        "url": form_data.url,
        "title": form_data.title,
        "description": form_data.description,
        "categories": categories,
        "creation_dt": str(datetime.datetime.now(tz=datetime.UTC)),
        "created_by": current_user["_id"],
    })

    # TODO (ames0k0): DRY
    # TODO (ames0k0): Unique categories
    # XXX (ames0k0): LIFO(`issues_ids`)
    for tag in categories["tags"]:
        db_ci_tag = await categories_collection.find_one({
            "identifiers": CCategoriesIdentifiersEnum.tags,
            "name": tag,
        })
        if db_ci_tag:
            await categories_collection.update_one(
                {"_id": ObjectId(db_ci_tag["_id"])},
                {"$set": {
                    "issues_ids": [
                        result.inserted_id
                    ] + db_ci_tag["issues_ids"],
                }}
            )
        else:
            await categories_collection.insert_one({
                "identifiers": CCategoriesIdentifiersEnum.tags,
                "name": tag,
                "issues_ids": [result.inserted_id]
            })

    for label in categories["labels"]:
        db_ci_label = await categories_collection.find_one({
            "identifier": CCategoriesIdentifiersEnum.labels,
            "name": label,
        })
        if db_ci_label:
            await categories_collection.update_one(
                {"_id": ObjectId(db_ci_label["_id"])},
                {"$set": {
                    "issues_ids": [
                        result.inserted_id
                    ] + db_ci_label["issues_ids"]
                }}
            )
        else:
            await categories_collection.insert_one({
                "identifiers": CCategoriesIdentifiersEnum.labels,
                "name": label,
                "issues_ids": [result.inserted_id]
            })

    redirect_url = request.url_for(
        "get_issues_new"
    ).include_query_params(
        error_message=f"Issues New Succeed; (#{result.inserted_id})",
    )
    return RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_303_SEE_OTHER,
    )


@issues_router.get("/delete/{issue_id}", name="get_issues_delete")
async def get_issues_delete(
    issue_id: str,
    request: Request,
    current_user=Depends(get_current_user),
):
    collection = await MongoDB.collection(DBCollectionsEnum.issues)
    db_issue = await collection.find_one({"_id": ObjectId(issue_id)})
    if not db_issue:
        redirect_url = request.url_for(
            "issues_get"
        ).include_query_params(
            error_message="Issues Delete Failed; No Issue Found.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_303_SEE_OTHER,
        )

    db_issue = IssuesModel(**db_issue)
    if db_issue.created_by != current_user["_id"]:
        redirect_url = request.url_for(
            "issues_get"
        ).include_query_params(
            error_message="Issues Delete Failed; Permissions Error.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return template_files.TemplateResponse(
        request=request,
        name="issues/issues_delete.html",
        context={
            "user": current_user,
            "issue": db_issue,
        }
    )


@issues_router.post("/delete/{issue_id}", name="post_issues_delete")
async def post_issues_delete(
    issue_id: str,
    request: Request,
    current_user=Depends(get_current_user),
):
    collection = await MongoDB.collection(DBCollectionsEnum.issues)
    db_issue = await collection.find_one({"_id": ObjectId(issue_id)})
    if not db_issue:
        redirect_url = request.url_for(
            "issues_get"
        ).include_query_params(
            error_message="Issues Delete Failed; No Issue Found.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_303_SEE_OTHER,
        )

    db_issue = IssuesModel(**db_issue)
    if db_issue.created_by != current_user["_id"]:
        redirect_url = request.url_for(
            "issues_get"
        ).include_query_params(
            error_message="Issues Delete Failed; Permissions Error.",
        )
        return RedirectResponse(
            url=redirect_url,
            status_code=status.HTTP_303_SEE_OTHER,
        )

    await collection.delete_one({"_id": ObjectId(issue_id)})

    redirect_url = request.url_for(
        "issues_get"
    ).include_query_params(
        error_message="Issues Delete Succeed.",
    )
    return RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_303_SEE_OTHER,
    )
