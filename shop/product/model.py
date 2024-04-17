from pydantic import Field

from databases.mongo_repository import MongoRepository, MongoUpdate


class Product(MongoRepository):
    name: str = Field(...)


class ProductUpdate(MongoUpdate):
    name: str
