from typing import List
from pydantic import Field

from product.model import MongoRepository, MongoUpdate


class ShoppingCart(MongoRepository):
    user_id: int = Field(...)
    product_ids: List[str] = Field(...)


class ShoppingUpdate(MongoUpdate):
    user_id: int
    product_ids: List[str]
