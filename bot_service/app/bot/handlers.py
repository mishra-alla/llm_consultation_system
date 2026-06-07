#app/bot/handlers.py
from aiogram import Router, types
from aiogram.filters import Command
from app.infra.redis import get_redis
from app.core.jwt import decode_and_validate
from app.tasks.llm_tasks import llm_request

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "👋 Вас приветствует Кузя!\n\n"
        "Чтобы со мной поговорить - надо авторизоваться:\n"
            "1. Зарегистрируйтесь в Auth Service Swagger\n"
            "2. Получите JWT-токен через /auth/login\n"
            "3. Отправьте команду: /token <ваш_jwt_token>"
        )

@router.message(Command("token"))
async def save_token(message: types.Message):
    token = message.text.replace("/token", "").strip()
    
    if not token:
        await message.answer("Usage: /token <JWT>")
        return
    
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("Неправильный или недействительный токен")
        return
    
    redis = await get_redis()
    await redis.set(f"token:{message.from_user.id}", token, ex=3600 * 24)
    await message.answer("Прекрасно - у меня есть ваш Токен, я его сохраню!\n"
                        "Я весь внимание - спрашивайте?")


@router.message()
async def ask_llm(message: types.Message):
    redis = await get_redis()
    token = await redis.get(f"token:{message.from_user.id}")
    
    if not token:
        await message.answer("Токен не найден. Отправьте, пожалуйста /token <JWT>")
        return
    
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("Срок действия токена истёк. Получите новый")
        await redis.delete(f"token:{message.from_user.id}")
        return
    
    llm_request.delay(message.from_user.id, message.text)
    await message.answer("Запрос отправлен ИИ - скоро вернусь с ответом")