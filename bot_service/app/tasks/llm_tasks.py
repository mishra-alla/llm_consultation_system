# app/tasks/llm_tasks.py
import asyncio
from celery import shared_task
from app.services.openrouter_client import call_openrouter


@shared_task(name="llm_request")
def llm_request(chat_id: int, prompt: str):
    """Celery задача для запроса к LLM"""
    result = asyncio.run(call_openrouter(prompt))
    # В реальном проекте здесь отправка ответа пользователю
    # Для учебного проекта - возвращаем результат
    return {"chat_id": chat_id, "response": result}
