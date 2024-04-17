from typing import List
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, status

from bson.errors import InvalidId

from .model import ShoppingCart, ShoppingUpdate

router = APIRouter()


@router.post("/", summary="Создать новую корзину", response_model=ShoppingCart)
def create_clothes(shopping_cart: ShoppingUpdate = Body(...)):
    print("Создаём новую корзину...", end='')
    shopping_cart = ShoppingCart(user_id=shopping_cart.user_id, product_ids=shopping_cart.product_ids).create()
    print(" успешно.")
    return shopping_cart


@router.get("/", summary="Получить список всех корзин", response_model=List[ShoppingCart])
def read_all(limit: int = 100, start_pos: int = 0):
    print("Запрос всех корзин...", end='')
    shopping_carts = ShoppingCart.read_all(limit=limit, start_pos=start_pos)
    print("  успешно")
    return shopping_carts


@router.get("/{id}", summary="Получить корзину по id", response_model=ShoppingCart)
def read(id: str):
    print(f"Запрос корзины с id = {id}...", end='')
    try:
        shopping_cart = ShoppingCart.read(id=ObjectId(id))
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    if shopping_cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Корзина с id {id} не найден")
    print(" успешно")
    return shopping_cart


@router.delete("/{id}", summary="Удалить корзину по id")
def delete(id: str):
    print(f"Удаление корзины с id = {id}...", end='')
    try:
        ShoppingCart.delete(id=ObjectId(id))
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    print(" успешно")
    return 'ok'
