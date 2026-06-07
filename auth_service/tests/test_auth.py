import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.base import Base
from app.db.session import engine


@pytest.fixture(scope="function")
async def client():
    """Создаём тестового клиента с чистой БД"""
    # Создаём таблицы для тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Создаём асинхронный клиент
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    # Очищаем после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Тест успешной регистрации"""
    response = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secret123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Тест регистрации с уже существующим email"""
    # Первая регистрация
    resp1 = await client.post(
        "/auth/register", 
        json={"email": "duplicate@example.com", "password": "pass"}
    )
    assert resp1.status_code == 201
    
    # Вторая с тем же email
    resp2 = await client.post(
        "/auth/register", 
        json={"email": "duplicate@example.com", "password": "pass"}
    )
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Тест успешного логина"""
    # Сначала регистрируемся
    await client.post(
        "/auth/register", 
        json={"email": "login@example.com", "password": "mypass"}
    )
    
    # Логинимся
    response = await client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "mypass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Тест логина с неверным паролем"""
    # Регистрируемся
    await client.post(
        "/auth/register", 
        json={"email": "wrong@example.com", "password": "correct"}
    )
    
    # Пробуем войти с неверным паролем
    response = await client.post(
        "/auth/login",
        data={"username": "wrong@example.com", "password": "wrong"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_endpoint_with_valid_token(client: AsyncClient):
    """Тест защищённого эндпоинта /auth/me с валидным токеном"""
    # Регистрация
    await client.post(
        "/auth/register", 
        json={"email": "me@example.com", "password": "pass"}
    )
    
    # Логин и получение токена
    login_resp = await client.post(
        "/auth/login", 
        data={"username": "me@example.com", "password": "pass"}
    )
    token = login_resp.json()["access_token"]
    
    # Запрос /me с токеном
    response = await client.get(
        "/auth/me", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["role"] == "user"


@pytest.mark.asyncio
async def test_me_endpoint_without_token(client: AsyncClient):
    """Тест /auth/me без токена"""
    response = await client.get("/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_endpoint_with_invalid_token(client: AsyncClient):
    """Тест /auth/me с неверным токеном"""
    response = await client.get(
        "/auth/me", 
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401
