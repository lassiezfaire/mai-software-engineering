import os
from datetime import datetime
import json
import random

import jwt
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException, status
from sqlmodel import Field, SQLModel, select
from sqlalchemy.exc import IntegrityError

from .db import session, redis_client
from .security import hash_password, check_password


class UserUpdate(SQLModel):
    name: str | None = None
    surname: str | None = None
    nickname: str | None = Field(unique=True, index=True)
    password: str | None = None


class UserBase(SQLModel):
    name: str
    surname: str
    nickname: str = Field(unique=True, index=True)
    password: str

    def create(self):
        self.password = hash_password(self.password)

        user = User.model_validate(self)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            return None
        return user

    @classmethod
    def auth(cls, nickname: str, password: str):
        statement = select(User).where(User.nickname == nickname)
        results = session.exec(statement)
        user = results.one()
        if not check_password(password=password, hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверный логин или пароль")

        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }

        payload = {
            "sub": user.nickname,
            "exp": datetime.now() + relativedelta(days=1)
        }

        token = jwt.encode(headers=headers,
                           payload=payload,
                           key=os.environ["SECRET_JWT"],
                           algorithm='HS256')

        return token

    @classmethod
    def read(cls, id: int):
        if redis_client.exists(id):
            json_user = redis_client.get(id)
            data_user = json.loads(json_user)
            print(f'Пользователь c id={id} прочитан из кэша')
            user = User(**data_user)
        else:
            user = session.get(User, id)
            json_user = user.json()
            redis_client.set(name=id, value=json_user)
            print(f'Пользователь c id={id} добавлен в кэш')
            redis_client.expire(name=id, time=3600)
        return user

    @classmethod
    def read_all(cls, limit: int = 100, start_pos: int = 0):
        statement = select(User).limit(limit).offset(start_pos)
        users = session.exec(statement).all()
        return users

    @classmethod
    def get_by_mask(cls, name_mask: str, surname_mask: str):
        statement = select(User).where(User.name.contains(name_mask),
                                       User.surname.contains(surname_mask))
        users = session.exec(statement).all()
        return users

    @classmethod
    def get_by_nick(cls, nickname: str):
        statement = select(User).where(User.nickname == nickname)
        results = session.exec(statement)
        user = results.one()
        return user

    @classmethod
    def get_random_cache(cls, limit: int = 100, start_pos: int = 0):
        id = random.randint(start_pos, limit)
        user = User.read(id=id)
        return user

    # @classmethod
    # def get_random(cls, limit: int = 100, start_pos: int = 0):
    #     id = random.randint(start_pos, limit)
    #     user = session.get(User, id)
    #     return user

    @classmethod
    def update(cls, id: int, user: UserUpdate):
        db_user = session.get(User, id)
        print(db_user)
        if not db_user:
            return None
        user_data = user.model_dump(exclude_unset=True)

        extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = hash_password(password)
            extra_data["password"] = hashed_password

        db_user.sqlmodel_update(user_data, update=extra_data)

        json_user = db_user.json()
        redis_client.set(name=id, value=json_user)
        redis_client.expire(name=id, time=3600)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @classmethod
    def delete(cls, id: int):
        user = session.get(User, id)
        if not user:
            return None
        session.delete(user)
        session.commit()
        return {"ok": True}


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
