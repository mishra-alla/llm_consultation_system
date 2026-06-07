# LLM Consultation System

Двухсервисная система для LLM-консультаций (через Telegram бота):

### **Цель проекта:** 
Разработка распределённой системы, состоящей из двух логически и технически независимых сервисов (каждый из которых выполняет строго определённую роль).

## Сервисы
- **Auth Service** - регистрация/аутентификация и выдача JWT токенов
- **Bot Service** - Telegram бот с авторизацией через JWT (предоставление LLM-консультаций через Telegram-бота)

## Технологии
- FastAPI, SQLite, JWT, bcrypt
- Aiogram, Celery, RabbitMQ, Redis
- OpenRouter API

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
    │   └── 01_messages_rates.png
    └── tests/
        ├── auth_service_test_results.txt
        └── auth_tests_pass.png
```
## Архитектура проекта
- **Auth Service**: регистрация, логин, выдача JWT
- **Bot Service**: Telegram bot + Celery + RabbitMQ + Redis
- LLM запросы уходят в очередь, обрабатываются воркером

## Запуск
docker-compose up --build

## Демонстрация работы Auth Service

### 1. Регистрация пользователя
![Регистрация](screenshots/auth_service/01_register_success.png)

### 2. Получение JWT токена
![Логин](screenshots/auth_service/02_login_success.png)

### 3. Проверка авторизации (/auth/me)
![Профиль пользователя](screenshots/auth_service/03_me_success.png)