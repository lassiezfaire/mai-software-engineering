from pydantic import Field

from product.model import Product, ProductUpdate


class Clothes(Product):
    type: str = Field(...)
    colour: str = Field(...)


class ClothesUpdate(ProductUpdate):
    type: str
    colour: str
