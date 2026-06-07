import asyncio
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from app.core.config import settings
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

# Создаём бота и диспетчер
bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("✅ Бот работает! Отправьте /token для авторизации")


@dp.message(Command("token"))
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
    await message.answer("✅ Токен сохранён!")


@dp.message()
async def ask_llm(message: types.Message):
    redis = await get_redis()
    token = await redis.get(f"token:{message.from_user.id}")
    
    if not token:
        await message.answer("❌ Токен не найден. Отправьте /token <JWT>")
        return
    
    try:
        decode_and_validate(token)
    except ValueError:
        await message.answer("❌ Токен истёк. Получите новый")
        await redis.delete(f"token:{message.from_user.id}")
        return
    
    llm_request.delay(message.from_user.id, message.text)
    await message.answer("🤔 Запрос отправлен ИИ...")


async def main():
    print(f"Starting bot {settings.app_name}...")
    print(f"Bot username: @kuzya2025_bot")
    
    # Удаляем webhook на всякий случай
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())