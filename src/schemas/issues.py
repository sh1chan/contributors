from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import AnyHttpUrl
from pydantic import AwareDatetime
from pydantic import model_validator
from pydantic import computed_field
from pydantic.types import StringConstraints
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
    created_by: ObjectId | None = Field(None)
    creation_dt: AwareDatetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


def seperate_field_values(field: str, delimiter: str = ',') -> list[str]:
    """ Returns unique field values
    """
    values = []

    if not field:
        return values

    for v in field.split(delimiter):
        v = v.strip().lower()
        if not v:
            continue
        values.append(v)

    return list(set(values))


class IssuesFiltersModel(BaseModel):
    title: str
    tags: str
    labels: str
    id: str
    created_by: str

    @model_validator(mode='after')
    def clean_up_fields(self) -> Self:
        self.title = self.title.strip()
        self.tags = self.tags.strip()
        self.labels = self.labels.strip()
        self.id = self.id.strip()
        self.created_by = self.created_by.strip()
        return self

    @computed_field
    @property
    def all_tags(self) -> list[str]:
        return seperate_field_values(self.tags)

    @computed_field
    @property
    def all_labels(self) -> list[str]:
        return seperate_field_values(self.labels)


class IssuesNewIn(BaseModel):
    url: Annotated[str, StringConstraints(strip_whitespace=True)]
    title: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1)
    ]
    description: Annotated[str, StringConstraints(strip_whitespace=True)]
    tags: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1)
    ]
    labels: Annotated[str, StringConstraints(strip_whitespace=True)]

    @model_validator(mode='after')
    def validate_tags_and_labels(self):
        for _ in seperate_field_values(self.tags):
            break
        else:
            raise ValueError('Issue `tags` are required!')

        return self

    @computed_field
    @property
    def all_tags(self) -> list[str]:
        return seperate_field_values(self.tags)

    @computed_field
    @property
    def all_labels(self) -> list[str]:
        return seperate_field_values(self.labels)
