#run_bot.pyrun_bot.py
#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.bot.dispatcher import bot, dp
from app.core.config import settings


async def main():
    print(f"Starting bot {settings.app_name}...")
    print(f"Bot token: {settings.telegram_bot_token[:10]}...")
    
    # Удаляем webhook 
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())