from jose import jwt, JWTError
from app.core.config import settings


def decode_and_validate(token: str) -> dict:
    """
    Декодирует и валидирует JWT токен.
    Только проверка, без создания!
    """
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret, 
            algorithms=[settings.jwt_alg]
        )
        
        # Проверяем наличие обязательных полей
        if "sub" not in payload:
            raise ValueError("Token missing 'sub' field")
        if "exp" not in payload:
            raise ValueError("Token missing 'exp' field")
            
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}")
