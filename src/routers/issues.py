from fastapi import APIRouter


issues_router = APIRouter(prefix="/issues", tags=["issues"])


@issues_router.get("/")
async def root_get():
    return {}
