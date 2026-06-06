from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Создаём таблицы в БД при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"{settings.app_name} started in {settings.env} mode")
    yield
    # Закрываем соединения при остановке
    await engine.dispose()
    print(f"uv run uvicorn app.main:app --reload --port 8000{settings.app_name} shut down")


app = FastAPI(
    title="Auth Service",
    description="Сервис аутентификации и выдачи JWT токенов",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(api_router)


@app.get("/health")
async def health():
    """Проверка здоровья сервиса"""
    return {"status": "ok", "app": settings.app_name}
