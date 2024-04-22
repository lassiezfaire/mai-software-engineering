from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from shopping_cart.db import create_db_and_tables
from shopping_cart.routes import router as cart_router

app = FastAPI()


@app.get("/", description="Точка входа", summary="Вход", include_in_schema=False)
def home_page():
    return RedirectResponse("/docs")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(cart_router, tags=["Корзины"], prefix="/cart")

# run fastapi app:
# uvicorn main:app --reload --host 0.0.0.0 --port 8002 --env-file environment.env
