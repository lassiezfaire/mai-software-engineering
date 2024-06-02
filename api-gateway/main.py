from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import router

app = FastAPI()


@app.get("/", description="Точка входа", summary="Вход", include_in_schema=False)
def home_page():
    return RedirectResponse("/docs")


app.include_router(router, tags=["API Gateway"], prefix="/gateway")

# run fastapi app:
# uvicorn main:app --reload --host 0.0.0.0 --port 8080 --env-file environment.env
