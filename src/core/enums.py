from enum import StrEnum
from enum import auto


class CookiesKeysEnum(StrEnum):
    access_token = auto()


class IssuesSupportedURLEnum(StrEnum):
    github = "github.com"


class DBCollectionsEnum(StrEnum):
    users = auto()
    projects = auto()
    issues = auto()
    categories = auto()


class CCategoriesIdentifiersEnum(StrEnum):
    tags = auto()
    labels = auto()
