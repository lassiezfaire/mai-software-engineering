from fastapi import FastAPI

from user.db import create_db_and_tables
from user.routes import router as user_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(user_router, tags=["Пользователи"], prefix="/user")

# run fastapi app:
# uvicorn main:app --reload --host 0.0.0.0 --env-file environment.env
