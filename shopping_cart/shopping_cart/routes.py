import os
from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from .model import Cart, CartCreate, CartRead
from .security import check_jwt

router = APIRouter()


@router.post("/", summary="Добавить товар в корзину (создать запись)", response_model=CartRead)
def create_entry(token: str, entry: CartCreate):
    if check_jwt(token=token, secret_key=os.environ["SECRET_JWT"]) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный токен")
    print("Создаём новую запись...", end='')
    entry = entry.add_to_cart()
    print(" успешно.")
    return entry


@router.get("/", summary="Получить список всех записей", response_model=List[CartRead])
def read_all_entries(token: str, limit: int = 100, start_pos: int = 0):
    if check_jwt(token=token, secret_key=os.environ["SECRET_JWT"]) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный токен")
    print("Запрос всех записей...", end='')
    entries = Cart.read_all(limit=limit, start_pos=start_pos)
    print(f" получено записей: {len(entries)}.")
    return entries


@router.get("/user/{user_id}/", summary="Получить корзину по id пользователя", response_model=List[CartRead])
def read_cart(token: str, user_id: int):
    if check_jwt(token=token, secret_key=os.environ["SECRET_JWT"]) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный токен")
    print("Запрос корзины...", end='')
    entries = Cart.read_by_user(user_id=user_id)
    print(f" получено записей: {len(entries)}.")
    return entries


# @router.get("/product/{product_id}/", summary="Получить записи по id товара", response_model=List[CartRead])
# def read_by_product(product_id: str):
#     print("Запрос записей...", end='')
#     entries = Cart.read_by_product(product_id=product_id)
#     print(f" получено записей: {len(entries)}.")
#     return entries


# @router.get("/{id}", summary="Получить запись по id", response_model=CartRead)
# def read_entry(id: int):
#     print(f"Запрос записи с id = {id}...", end='')
#     entry = Cart.read(id)
#     print(" успешно")
#     return entry


@router.delete('/{id}', summary="Удалить запись по id")
def delete_entry(token: str, id: int):
    if check_jwt(token=token, secret_key=os.environ["SECRET_JWT"]) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный токен")
    print(f"Удаление записи с id = {id}...", end='')
    deleted = Cart.delete(id)
    print(" успешно")
    return deleted


@router.delete("/user/{user_id}/", summary="Удалить корзину по id пользователя")
def read_cart(token: str, user_id: int):
    if check_jwt(token=token, secret_key=os.environ["SECRET_JWT"]) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный токен")
    print(f"Удаление корзины пользователя с id = {user_id}...", end='')
    deleted = Cart.delete_by_user(user_id=user_id)
    print(f" успешно.")
    return deleted


@router.delete("/product/{product_id}/", summary="Удалить записи по id товара")
def read_cart(token: str, product_id: str):
    if check_jwt(token=token, secret_key=os.environ["SECRET_JWT"]) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный токен")
    print(f"Удаление корзины пользователя с id = {product_id}...", end='')
    deleted = Cart.delete_by_product(product_id=product_id)
    print(f" успешно.")
    return deleted
