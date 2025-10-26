from fastapi import APIRouter


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/register")
async def register_get():
    return {}


@auth_router.post("/register")
async def register_post():
    return {}
