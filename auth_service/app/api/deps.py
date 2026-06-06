from typing import Annotated
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUsecase
from app.core.security import decode_token
from app.core.exceptions import InvalidTokenError, TokenExpiredError


async def get_db() -> AsyncSession:
    """Зависимость для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Зависимость для получения репозитория пользователей"""
    return UserRepository(db)


async def get_auth_uc(repo: UserRepository = Depends(get_user_repo)) -> AuthUsecase:
    """Зависимость для получения usecase аутентификации"""
    return AuthUsecase(repo)


async def get_current_user_id(
    authorization: Annotated[str | None, Header()] = None
) -> int:
    """Зависимость для получения ID текущего пользователя из JWT"""
    if not authorization or not authorization.startswith("Bearer "):
        raise InvalidTokenError()

    token = authorization[7:]  # Убираем "Bearer "
    
    try:
        payload = decode_token(token)
    except ValueError:
        raise InvalidTokenError()

    # Проверяем наличие exp
    if "exp" not in payload:
        raise InvalidTokenError()

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError()

    return int(user_id)
