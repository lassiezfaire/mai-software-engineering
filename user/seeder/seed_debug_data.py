from user.db import create_db_and_tables, engine
from user.model import User


def initialize_db():
    # clearing tables
    User.__table__.drop(engine)

    # creating tables we need
    create_db_and_tables()


def seed_users():
    user1 = User(name='John', surname='Smith', nickname='johnsmith8', password='changeme')
    user1.create()
    user2 = User(name='Ivan', surname='Ivanov', nickname='ivan.ivanov', password='12345')
    user2.create()
    user3 = User(name='Laissez', surname='Faire', nickname='lassiezfaire6', password='amdevs')
    user3.create()


initialize_db()
seed_users()
