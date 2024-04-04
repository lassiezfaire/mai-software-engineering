from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from .model import User, UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("/", summary="Создать нового пользователя", response_model=UserRead)
def create_user(user: UserCreate):
    print("Создаём нового пользователя...", end='')
    try:
        created_user = user.create()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Пользователь с таким никнеймом уже существует")
    print(" успешно.")
    return created_user


@router.get("/{id}", summary="Получить пользователя по id", response_model=UserRead)
def read_user(id: int):
    print(f"Запрос пользователя с id = {id}...", end='')
    if (user := User.read(id)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id = {id} не найден")
    print(" успешно")
    return user


@router.get("/", summary="Получить список всех пользователей", response_model=List[UserRead])
def read_all_users(limit: int = 100):
    print("Запрос всех пользователей...", end='')
    users = User.read_all(limit=limit)
    print(f" получено записей: {len(users)}.")
    return users


@router.get("/name_find/", summary="Найти пользователей по маске имени и фамилии", response_model=List[UserRead])
def find_by_name(name_mask: str, surname_mask: str):
    print(f"Запрос пользователей по маске имени {name_mask} и маске фамилии {surname_mask}...", end='')
    users = User.get_by_mask(name_mask=name_mask, surname_mask=surname_mask)
    print(f" найдено записей: {len(users)}.")
    return users


@router.get("/nick_find/", summary="Найти пользователя по никнейму", response_model=UserRead)
def find_by_nick(nickname: str):
    print(f"Запрос пользователя с никнеймом {nickname}...", end='')
    try:
        user = User.get_by_nick(nickname=nickname)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Пользователь с никнеймом {nickname} не найден")
    print(" успешно")
    return user


@router.patch("/{id}", summary="Обновить данные пользователя по id", response_model=UserRead)
def update_user(id: int, user: UserUpdate):
    print(f"Обновление данные пользователя с id = {id}...", end='')
    if (user := User.update(id, user)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id = {id} не найден")
    print(" успешно")
    return user


@router.delete('/{id}', summary="Удалить пользователя по id")
def delete_user(id: int):
    print(f"Удаление данных пользователя с id = {id}...", end='')
    if (deleted := User.delete(id)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id = {id} не найден")
    print(" успешно")
    return deleted
