from fastapi import HTTPException, status

class BaseHTTPException(HTTPException):
    pass


class UserAlreadyExistsError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует"
        )


class InvalidCredentialsError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный email или password"
        )


class InvalidTokenError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный или некорректный token"
        )


class TokenExpiredError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token просрочен"
        )


class UserNotFoundError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )


class PermissionDeniedError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Отказано в доступе"
        )
