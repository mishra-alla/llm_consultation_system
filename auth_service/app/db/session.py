from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Асинхронный движок
engine = create_async_engine(
    settings.database_url,
    echo=True,              # Включаем логирование SQL-запросов для отладки
)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
