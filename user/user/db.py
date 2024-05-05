import os

from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv('../production/environment.env')

POSTGRES_URI = os.getenv('POSTGRES_URI')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASS = os.getenv('POSTGRES_PASS')

db_name = 'online_shop'
connection_string = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_URI}/{db_name}'

engine = create_engine(connection_string, echo=True)

session = Session(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
