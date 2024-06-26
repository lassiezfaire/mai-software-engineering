from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from user.db import create_db_and_tables
from user.routes import router as user_router

app = FastAPI()


@app.get("/", description="Точка входа", summary="Вход", include_in_schema=False)
def home_page():
    return RedirectResponse("/docs")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(user_router, tags=["Пользователи"], prefix="/user")

# run fastapi app:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000 --env-file environment.env
