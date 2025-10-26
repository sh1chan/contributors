from enum import StrEnum
from enum import auto

import pymongo
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase


class DBCollectionsEnum(StrEnum):
    users = auto()
    projects = auto()
    issues = auto()


class MongoDB:
    client: pymongo.AsyncMongoClient | None = None
    database: AsyncDatabase | None = None

    @classmethod
    async def initialize(cls):
        cls.client = pymongo.AsyncMongoClient(
            "mongodb://root:example@172.17.0.1:27017"
            # host="0.0.0.0", port=27017,
        )
        cls.database = getattr(cls.client, "contributors")

    @classmethod
    async def collection(cls, name: DBCollectionsEnum) -> AsyncCollection:
        return getattr(cls.database, name)
