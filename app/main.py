from fastapi import FastAPI
from app.db_setup import initialize_db
from app.routers import router as secrets_router

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    """
    Инициализация базы данных при запуске приложения.
    """
    await initialize_db()


app.include_router(secrets_router)


@app.get("/")
async def read_root():
    """
    Простая проверка работы сервиса.
    """
    return {"message": "Привет, я умею хранить секреты!"}
