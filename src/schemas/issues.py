from bson import ObjectId
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import AnyHttpUrl
from pydantic import AwareDatetime
from pydantic import model_validator
from pydantic import computed_field
from typing_extensions import Self


class IssuesCategoriesModel(BaseModel):
    tags: list[str] = Field([])
    labels: list[str] = Field([])


class IssuesModel(BaseModel):
    id: ObjectId = Field(..., alias="_id")
    url: AnyHttpUrl | str = Field("")
    title: str
    description: str | None = Field(None)
    # TODO (ames0k0): Remove old data
    categories: IssuesCategoriesModel | None = Field(None)
    projects: list[ObjectId] = Field([])
    added_by: ObjectId | None = Field(None)
    created_by: ObjectId | None = Field(None)
    creation_dt: AwareDatetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class IssuesNewIn(BaseModel):
    url: str
    title: str
    description: str
    tags: str
    labels: str

    @staticmethod
    def seperate_field_values(field: str, delimiter: str = ',') -> list[str]:
        if not field:
            return []
        return [v.strip() for v in field.split(delimiter)]

    @model_validator(mode='after')
    def clean_up_fields(self) -> Self:
        self.url = self.url.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()
        self.tags = self.tags.strip()
        self.labels = self.labels.strip()
        return self

    @computed_field
    @property
    def all_tags(self) -> list[str]:
        return self.seperate_field_values(self.tags)

    @computed_field
    @property
    def all_labels(self) -> list[str]:
        return self.seperate_field_values(self.labels)
