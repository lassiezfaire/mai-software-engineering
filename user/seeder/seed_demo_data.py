from faker import Faker
from sqlalchemy.exc import IntegrityError

from user.db import create_db_and_tables, engine
from user.model import User

fake = Faker()


def initialize_db():
    # clearing tables
    User.__table__.drop(engine)

    # creating tables we need
    create_db_and_tables()


def seed_users():
    for _ in range(1000):
        name = fake.first_name()
        surname = fake.last_name()
        nickname = fake.user_name()
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        user = User(name=name, surname=surname, nickname=nickname, password=password)
        try:
            user.create()
        except IntegrityError:
            pass


initialize_db()
seed_users()
