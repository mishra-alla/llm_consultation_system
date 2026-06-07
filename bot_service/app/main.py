#app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infra.redis import close_redis
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    print(f"{settings.app_name} started in {settings.env} mode")
    print(f"Redis URL: {settings.redis_url}")
    print(f"RabbitMQ URL: {settings.rabbitmq_url}")
    print(f"OpenRouter Model: {settings.openrouter_model}")
    yield
    # Закрываем соединения при остановке
    await close_redis()
    print(f"{settings.app_name} shut down")


app = FastAPI(
    title="Bot Service",
    description="Telegram bot with JWT auth, Celery, RabbitMQ, Redis",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health():
    """Проверка здоровья сервиса"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.env
    }


@app.get("/info")
async def info():
    """Информация о сервисе"""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "redis": settings.redis_url,
        "rabbitmq": settings.rabbitmq_url,
        "openrouter_model": settings.openrouter_model
    }