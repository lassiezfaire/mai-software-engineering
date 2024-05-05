import os
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, status

from bson.errors import InvalidId

from .model import Clothes, ClothesUpdate
from product.security import check_jwt

router = APIRouter()


@router.post("/", summary="Создать новый предмет одежды", response_model=Clothes)
def create_clothes(token: str, clothes: ClothesUpdate = Body(...)):
    check_jwt(token=token, secret_key=os.environ["SECRET_JWT"])
    print("Создаём новый предмет одежды...", end='')
    clothes = Clothes(name=clothes.name, type=clothes.type, colour=clothes.colour).create()
    print(" успешно.")
    return clothes


@router.get("/", summary="Получить список всех предметов одежды", response_model=List[Clothes])
def read_all(token: str, limit: int = 100, start_pos: int = 0):
    check_jwt(token=token, secret_key=os.environ["SECRET_JWT"])
    print("Запрос всех предметов одежды...", end='')
    clothes = Clothes.read_all(limit=limit, start_pos=start_pos)
    print("  успешно")
    return clothes


@router.get("/{id}", summary="Получить предмет одежды по id", response_model=Clothes)
def read(str, id: str):
    print(f"Запрос предмета одежды с id = {id}...", end='')
    try:
        clothes = Clothes.read(id=ObjectId(id))
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    if clothes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Товар с id {id} не найден")
    print(" успешно")
    return clothes


@router.patch("/{id}", summary="Изменить предмет одежды по id")
def update(token: str, id: str, clothes: ClothesUpdate):
    check_jwt(token=token, secret_key=os.environ["SECRET_JWT"])
    print(f"Обновление предмета одежды с id = {id}...", end='')
    try:
        clothes = Clothes.update(id=ObjectId(id), item=clothes)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    print(" успешно")
    return clothes


@router.delete("/{id}", summary="Удалить предмет одежды по id")
def delete(token: str, id: str):
    check_jwt(token=token, secret_key=os.environ["SECRET_JWT"])
    print(f"Обновление предмета одежды с id = {id}...", end='')
    print(f"Удаление предмета одежды с id = {id}...", end='')
    try:
        Clothes.delete(id=ObjectId(id))
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"{id} не является корректным ObjectId")
    print(" успешно")
    return 'ok'
