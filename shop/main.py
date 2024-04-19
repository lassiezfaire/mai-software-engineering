from fastapi import FastAPI

from product.routes import router as product_router
from products.routes import router as products_router
from shopping_cart.routes import router as shopping_cart_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    pass


# app.include_router(product_router, tags=["Товары"], prefix="/product")
app.include_router(products_router, tags=["Одежда"], prefix="/clothes")
app.include_router(shopping_cart_router, tags=["Корзины"], prefix="/shoppingcarts")

# run fastapi app:
# uvicorn main:app --reload --host 0.0.0.0 --port 8001 --env-file environment.env
