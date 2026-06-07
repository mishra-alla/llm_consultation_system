import pytest
from app.db.base import Base
from app.db.session import engine


@pytest.fixture(scope="function")
async def db_session():
    """Фикстура для чистой БД в каждом тесте"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Здесь можно создать сессию если надо
    
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
