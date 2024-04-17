from fastapi import FastAPI

from product.routes import router as product_router
from products.routes import router as products_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    pass


# app.include_router(product_router, tags=["Товары"], prefix="/product")
app.include_router(products_router, tags=["Одежда"], prefix="/clothes")

# run fastapi app:
# uvicorn main:app --reload --host 0.0.0.0 --env-file environment.env
