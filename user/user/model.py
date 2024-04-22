from sqlmodel import Field, SQLModel, Session, select
import bcrypt

from .db import engine


def hash_password(password: str) -> str:
    password_bytes = str.encode(password, encoding='utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return str(hashed_password)


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

        with Session(engine) as session:
            db_user = User.model_validate(self)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    @classmethod
    def read(cls, id: int):
        with Session(engine) as session:
            user = session.get(User, id)
            return user

    @classmethod
    def read_all(cls, limit: int = 100, start_pos: int = 0):
        with Session(engine) as session:
            statement = select(User).limit(limit).offset(start_pos)
            users = session.exec(statement).all()
            return users

    @classmethod
    def get_by_mask(cls, name_mask: str, surname_mask: str):
        with Session(engine) as session:
            statement = select(User).where(User.name.contains(name_mask),
                                           User.surname.contains(surname_mask))
            users = session.exec(statement).all()
            return users

    @classmethod
    def get_by_nick(cls, nickname: str):
        with Session(engine) as session:
            statement = select(User).where(User.nickname == nickname)
            results = session.exec(statement)
            user = results.one()
            return user

    @classmethod
    def update(cls, id: int, user: UserUpdate):
        with Session(engine) as session:
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
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

    @classmethod
    def delete(cls, id: int):
        with Session(engine) as session:
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
