# app/tasks/llm_tasks.py
import asyncio
from celery import shared_task
from app.services.openrouter_client import call_openrouter
from aiogram import Bot
from app.core.config import settings

# Создаём экземпляр бота для отправки сообщений
bot = Bot(token=settings.telegram_bot_token)


@shared_task(name="llm_request")
def llm_request(chat_id: int, prompt: str):
    """Celery задача для запроса к LLM и отправки ответа пользователю"""
    try:
        # Получаем ответ от OpenRouter
        result = asyncio.run(call_openrouter(prompt))
        
        # Отправляем ответ пользователю через бота
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.send_message(chat_id, f" {result}"))
        loop.close()
        
        print(f" Ответ отправлен пользователю {chat_id}")
        return {"chat_id": chat_id, "response": result, "status": "success"}
        
    except Exception as e:
        print(f" Ошибка в задаче: {e}")
        # Сообщаем пользователю об ошибке
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot.send_message(chat_id, f" Ошибка: {str(e)}"))
            loop.close()
        except:
            pass
        raise