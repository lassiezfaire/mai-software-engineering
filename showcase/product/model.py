from bson import ObjectId as _ObjectId
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from .db import database


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


ObjectId = Annotated[str, AfterValidator(check_object_id)]


class ProductUpdate(BaseModel):
    name: str


class Product(BaseModel):
    id: ObjectId | None = Field(alias="_id", default_factory=ObjectId)
    name: str = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    @classmethod
    def collection_name(cls):
        return cls.__name__

    def create(self):
        collection = self.collection_name()
        inserted = database[collection].insert_one(self.model_dump(by_alias=True, exclude={"id"}))
        item = database[collection].find_one({"_id": inserted.inserted_id})
        item['_id'] = str(item['_id'])
        return item

    @classmethod
    def read_all(cls, limit: int = 100, start_pos: int = 0):
        collection = cls.collection_name()
        items = list(database[collection].find(limit=limit).skip(start_pos))
        for item in items:
            item['_id'] = str(item['_id'])
        return items

    @classmethod
    def read(cls, id: ObjectId):
        collection = cls.collection_name()
        item = database[collection].find_one({"_id": id})
        if item is None:
            return item
        item['_id'] = str(item['_id'])
        return item

    @classmethod
    def update(cls, id: ObjectId, item: ProductUpdate):
        collection = cls.collection_name()
        item = database[collection].update_one({'_id': id},
                                               {'$set': item.model_dump(exclude={"id"})}, upsert=True)
        item = database[collection].find_one({"_id": id})
        item['_id'] = str(item['_id'])
        return item

    @classmethod
    def delete(cls, id: ObjectId):
        collection = cls.collection_name()
        deleted = database[collection].delete_one({"_id": id})
        return deleted

    @classmethod
    def get_random(cls):
        collection = cls.collection_name()
        pipeline = [{'$sample': {'size': 1}}]
        items = list(database[collection].aggregate(pipeline))
        if not items:
            return None
        item = items[0]
        item['_id'] = str(item['_id'])
        return item
