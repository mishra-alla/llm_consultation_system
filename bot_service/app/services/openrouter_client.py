import httpx
from app.core.config import settings


async def call_openrouter(prompt: str) -> str:
    """
    Отправляет запрос к OpenRouter API и возвращает ответ.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.openrouter_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": settings.openrouter_site_url,
                    "X-Title": settings.openrouter_app_name,
                },
                json={
                    "model": settings.openrouter_model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            
            # Извлекаем текст ответа
            return data["choices"][0]["message"]["content"]
            
        except httpx.TimeoutException:
            raise Exception("OpenRouter API timeout")
        except httpx.HTTPStatusError as e:
            raise Exception(f"OpenRouter API error: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
