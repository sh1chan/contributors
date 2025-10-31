from bson import ObjectId
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import AnyHttpUrl
from pydantic import AwareDatetime


class IssuesModel(BaseModel):
    id: ObjectId = Field(..., alias="_id")
    url: AnyHttpUrl | None
    title: str
    description: str | None = Field(None)
    tags: list[ObjectId] = Field([])
    labels: list[ObjectId] = Field([])
    projects: list[ObjectId] = Field([])
    added_by: ObjectId | None = Field(None)
    created_by: ObjectId | None = Field(None)
    creation_dt: AwareDatetime

    model_config = ConfigDict(arbitrary_types_allowed=True)
