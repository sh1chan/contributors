from fastapi import APIRouter


projects_router = APIRouter(prefix="/projects", tags=["projects"])


@projects_router.get("/")
async def root_get():
    return {}
