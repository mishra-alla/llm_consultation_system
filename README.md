# LLM Consultation System

Двухсервисная система для LLM-консультаций (через Telegram бота):

### **Цель проекта:** 
Разработка распределённой системы, состоящей из двух логически и технически независимых сервисов (каждый из которых выполняет строго определённую роль).

## Сервисы
- **Auth Service** - регистрация/аутентификация и выдача JWT токенов
- **Bot Service** - Telegram бот с авторизацией через JWT (предоставление LLM-консультаций через Telegram-бота)

## Технологии
- **Auth_Service**: FastAPI, SQLAlchemy, JWT, bcrypt
- **Bot_Service**: aiogram, Celery, Redis, RabbitMQ
- **LLM_API**: OpenRouter (бесплатные модели)

## Требования

- Docker Desktop (для RabbitMQ и Redis)
- Python 3.11+
- uv (менеджер пакетов)
- Telegram Bot Token (от @BotFather)
- OpenRouter API Key

## Структура проекта:
```
llm_consultation_system/
├── README.md
├── .gitignore
├── docker-compose.yml
├── auth_service/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── uv.lock
├── bot_service/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   └── uv.lock
└── screenshots/
    ├── auth_service/
    │   ├── 01_register_success.png
    │   ├── 02_login_success.png
    │   └── 03_me_success.png
    ├── bot_service/
    │   └── 01_bot_chat.png 
    ├── rabbitmq/
    │   └── 01_queues.png
    └── tests/
        ├── auth_service_test_results.txt   # текстовый вывод pytest
        ├── auth_service_coverage.txt       # покрытие кода
        ├── auth_tests_pass.png             # скриншот 7 passed (Auth)
        └── bot_tests_pass.png              # скриншот 3 passed (Bot)
```

## Установка и запуск
docker-compose up --build
#### 1. Клонирование репозитория
```
git clone https://github.com/mishra-alla/llm_consultation_system.git
cd llm_consultation_system
```
#### 2. Настройка переменных окружения
- **Auth Service (auth_service/.env):**
```
APP_NAME=auth-service
ENV=local
JWT_SECRET=your_super_secret_key_123
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
SQLITE_PATH=./auth.db
```
- **Bot Service (bot_service/.env):**
```
APP_NAME=bot-service
ENV=local
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
JWT_SECRET=your_super_secret_key_123
JWT_ALG=HS256
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672//
OPENROUTER_API_KEY=ваш_ключ_OpenRouter
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
```
*Важно: JWT_SECRET должен быть одинаковым в обоих сервисах!*

#### 3. Запуск инфраструктуры (Redis + RabbitMQ)
docker-compose up -d
docker-compose ps

#### 4. Запуск Auth Service
```
cd auth_service
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .
uv run uvicorn app.main:app --reload --port 8000
```
> Swagger документация: http://localhost:8000/docs
#### 5. Запуск Celery Worker (обработка задач LLM)
В новом терминале:
```
cd bot_service
source .venv/bin/activate
uv run celery -A app.infra.celery_app worker --loglevel=info
```
#### 6. Запуск Telegram Бота
В новом терминале:
```
cd bot_service
source .venv/bin/activate
uv run python run_bot.py
```
## Использование
#### 1. Получение JWT токена
- Откройте Swagger Auth Service: http://localhost:8000/docs
  - POST /auth/register - зарегистрируйтесь с email (формат: surname@email.com)
  - POST /auth/login - войдите и скопируйте access_token

#### 2. Авторизация в боте
В Telegram боте @kuzya2025_bot отправьте:
```/token <ваш_jwt_токен>```
#### 3. Общение с LLM
Просто отправьте любой текст боту. Он ответит через нейросеть.

## Демонстрация работы Auth_Service

### 1. Регистрация пользователя
![Регистрация](screenshots/auth_service/01_register_success.png)

### 2. Получение JWT токена
![Логин](screenshots/auth_service/02_login_success.png)

### 3. Проверка авторизации (/auth/me)
![Профиль пользователя](screenshots/auth_service/03_me_success.png)

## Демонстрация работы Bot_Service

### Bot_Service
![Bot_Service](screenshots/bot_service/01_telegram_dialogue.png)

### RabbitMQ
![RabbitMQ Queues](screenshots/rabbitmq/01_queues.png)

## Тестирование
Для проверки проекта использовалось автоматизированное тестирование.
> Результаты можно посмотреть: /screenshots/tests/

Пример запуска тестов:
```
cd ../auth_service
uv run pytest

cd ../bot_service
uv run pytest
```
## Автор: 
**Алла Мишра: mishra-alla**