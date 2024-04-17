from typing import List
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, status

from bson.errors import InvalidId

from .model import Product, ProductUpdate

router = APIRouter()


@router.post("/", summary="Создать новой товар", response_model=Product)
def create_product(product: ProductUpdate = Body(...)):
    print("Создаём новый товар...", end='')
    product = Product(name=product.name).create()
    print(" успешно.")
    return product


@router.get("/", summary="Получить список всех товаров", response_model=List[Product])
def read_all(limit: int = 100, start_pos: int = 100):
    print("Запрос всех товаров...", end='')
    products = Product.read_all(limit=limit, start_pos=start_pos)
    print("  успешно")
    return products


@router.get("/{id}", summary="Получить товар по id", response_model=Product)
def read(id: str):
    print(f"Запрос товара с id = {id}...", end='')
    try:
        product = Product.read(id=ObjectId(id))
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Товар с id {id} не найден")
    print(" успешно")
    return product


@router.patch("/{id}", summary="Изменить товар по id")
def update(id: str, product: ProductUpdate):
    print(f"Обновление данных товара с id = {id}...", end='')
    try:
        product = Product.update(id=ObjectId(id), item=product)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    print(" успешно")
    return product


@router.delete("/{id}", summary="Удалить товар по id")
def delete(id: str):
    print(f"Удаление данных товара с id = {id}...", end='')
    try:
        Product.delete(id=ObjectId(id))
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    print(" успешно")
    return 'ok'
