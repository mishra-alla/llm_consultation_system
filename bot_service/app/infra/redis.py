import redis.asyncio as redis
from app.core.config import settings

_redis_client = None


async def get_redis() -> redis.Redis:
    """Возвращает асинхронный Redis клиент (синглтон)"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
            max_connections=10
        )
    return _redis_client


async def close_redis():
    """Закрывает Redis соединение"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
