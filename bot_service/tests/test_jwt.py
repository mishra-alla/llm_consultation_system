# tests/test_jwt.py
import pytest
from app.core.jwt import decode_and_validate
from jose import jwt
from app.core.config import settings


def test_decode_valid_token():
    """Тест валидации корректного токена"""
    # Создаём тестовый токен
    token = jwt.encode(
        {"sub": "123", "role": "user", "exp": 9999999999},
        settings.jwt_secret,
        algorithm=settings.jwt_alg
    )
    
    payload = decode_and_validate(token)
    assert payload["sub"] == "123"
    assert payload["role"] == "user"


def test_decode_invalid_token():
    """Тест с неверным токеном"""
    with pytest.raises(ValueError, match="Invalid token"):
        decode_and_validate("invalid.token.here")


def test_decode_expired_token():
    """Тест с просроченным токеном"""
    from datetime import datetime, timedelta, timezone
    import time
    
    # Создаём просроченный токен
    exp_time = datetime.now(timezone.utc) - timedelta(seconds=1)
    token = jwt.encode(
        {"sub": "123", "exp": exp_time},
        settings.jwt_secret,
        algorithm=settings.jwt_alg
    )
    
    with pytest.raises(ValueError):
        decode_and_validate(token)