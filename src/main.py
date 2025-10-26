from fastapi import FastAPI

from src.routers.auth import auth_router
from src.routers.projects import projects_router
from src.routers.issues import issues_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(issues_router)
