from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from products.routes import router as products_router

app = FastAPI()


@app.get("/", description="Точка входа", summary="Вход", include_in_schema=False)
def home_page():
    return RedirectResponse("/docs")


app.include_router(products_router, tags=["Одежда"], prefix="/clothes")

# run fastapi app:
# uvicorn main:app --reload --host 0.0.0.0 --port 8001 --env-file environment.env
