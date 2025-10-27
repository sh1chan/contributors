from typing import Annotated

from pydantic import BaseModel
from fastapi import Form


class RegisterFormIn(BaseModel):
    username: Annotated[str, Form()]
    password: Annotated[str, Form()]


class TokenData(BaseModel):
    username: str | None = None


class TokenOut(BaseModel):
    access_token: str
    token_type: str
