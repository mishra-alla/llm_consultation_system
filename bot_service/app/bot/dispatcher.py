from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from app.core.config import settings

# from aiohttp_socks import ProxyConnector
# from aiohttp import ClientSession


# --- Настройка прокси ---
# Берём данные прокси из вашего файла .env
# proxy_url = settings.proxy_url
# proxy_password = settings.proxy_password

# Создаём специальный коннектор для SOCKS5 прокси
# Обратите внимание, как вставляется пароль — без логина.
# Формат: socks5://host:port
# connector = ProxyConnector.from_url(proxy_url, password=proxy_password)

# # Создаём HTTP-сессию с этим коннектором
# client_session = ClientSession(connector=connector)

# # Создаём сессию aiogram на основе нашей HTTP-сессии
# telegram_session = AiohttpSession(session=client_session)

# # --- Создаём бота ---
# # Передаём готовую сессию с прокси в конструктор Bot
# bot = Bot(token=settings.telegram_bot_token, session=telegram_session)
# dp = Dispatcher()


# Проверяем, настроен ли прокси
# if settings.proxy_url and settings.proxy_password:
#     try:
#         # Разбираем URL прокси
#         proxy_url = settings.proxy_url
#         # Убираем префикс socks5:// если есть
#         if proxy_url.startswith('socks5://'):
#             proxy_host = proxy_url.replace('socks5://', '')
#         else:
#             proxy_host = proxy_url
        
#         # Разделяем хост и порт
#         if ':' in proxy_host:
#             host, port = proxy_host.split(':')
#             port = int(port)
#         else:
#             host = proxy_host
#             port = 443
        
#         # Создаём коннектор вручную (без password в from_url)
#         # Используем другой метод создания коннектора
#         connector = ProxyConnector(
#             proxy_type=5,  # SOCKS5
#             host=host,
#             port=port,
#             password=settings.proxy_password
#         )
#         client_session = ClientSession(connector=connector)
#         telegram_session = AiohttpSession(session=client_session)
#         print(f"Proxy configured: {host}:{port}")
#     except Exception as e:
#         print(f"Proxy error: {e}, starting without proxy")
#         telegram_session = AiohttpSession()
# else:
#     print("No proxy configured, starting directly")

# Создаём сессию
session = AiohttpSession()

# Создаём бота
bot = Bot(token=settings.telegram_bot_token, session=session)

# Создаём диспетчер
dp = Dispatcher()

print("Bot dispatcher initialized")
