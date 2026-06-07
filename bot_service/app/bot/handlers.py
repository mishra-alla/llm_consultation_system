#app/bot/handlers.py
from aiogram import Router, types
from aiogram.filters import Command
from app.infra.redis import get_redis
from app.core.jwt import decode_and_validate
from app.tasks.llm_tasks import llm_request

router = Router()

# @router.message(Command("start"))
# async def start(message: types.Message):
#     await message.answer("Привет! Я бот КУЗЯ!")

@router.message(Command("start"))
async def start(message: types.Message):
    """Приветствие"""
    await message.answer(
        "Бот работает!\n\n"
        "Инструкция:\n"
        "1. Получите JWT токен в Auth Service\n"
        "2. Отправьте команду /token <ваш_токен>\n"
        "3. Задавайте вопросы"
    )


@router.message(Command("token"))
async def save_token(message: types.Message):
    """Сохраняет JWT токен в Redis"""
    token = message.text.replace("/token", "").strip()
    
    if not token:
        await message.answer("Usage: /token <JWT>")
        return
    
    # Валидация токена
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("Неправильный или недействительный токен. Пожалуйста, получите новый токен в Auth Service.")
        return
    
    # Сохраняем в Redis
    redis = await get_redis()
    await redis.set(f"token:{message.from_user.id}", token, ex=3600 * 24)
    await message.answer("Токен сохранён! Теперь вы можете задавать вопросы.")


@router.message()
async def ask_llm(message: types.Message):
    """Обработка текстовых сообщений"""
    redis = await get_redis()
    token = await redis.get(f"token:{message.from_user.id}")
    
    if not token:
        await message.answer(
            "Токен не найден. Сначала пройдите аутентификацию:\n"
            "1. Зарегистрируйтесь в Auth Service Swagger\n"
            "2. Получите JWT-токен по адресу /auth/login\n"
            "3. Отправьте /token <ваш_jwt>"
        )
        return
    
    # Валидация токена
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("Срок действия токена истек или он недействителен. Пожалуйста, получите новый токен.")
        await redis.delete(f"token:{message.from_user.id}")
        return
    
    # Отправляем задачу в Celery
    try:
        llm_request.delay(message.from_user.id, message.text)
        await message.answer("Запрос отправлен ИИ. Обработка запроса")
    except Exception as e:
        await message.answer(f"Ошибка отправки задачи: {str(e)}")