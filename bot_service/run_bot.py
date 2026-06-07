#run_bot.pyrun_bot.py
#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

# Добавляем app
sys.path.insert(0, str(Path(__file__).parent))

from app.bot.dispatcher import bot, dp
from app.core.config import settings


async def main():
    """Запуск Telegram-бота в polling режиме"""
    print(f"Starting bot {settings.app_name}...")
    print(f"Bot token: {settings.telegram_bot_token[:10]}...")
    
    try:
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())