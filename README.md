# LLM Consultation System
Двухсервисная система для LLM-консультаций (через Telegram бота):
**Цель проекта:** Разработка распределённой системы, состоящей из двух логически и технически независимых сервисов (каждый из которых выполняет строго определённую роль).

## Сервисы
- **Auth Service** - регистрация/аутентификация и выдача JWT токенов
- **Bot Service** - Telegram бот с авторизацией через JWT (предоставление LLM-консультаций через Telegram-бота)

## Технологии
- FastAPI, SQLite, JWT, bcrypt
- Aiogram, Celery, RabbitMQ, Redis
- OpenRouter API

## Структура проекта:
```
final_project/
├── auth_service/
│   ├── app/
│   ├── tests/
│   ├── .env
│   ├── pyproject.toml
│   └── pytest.ini
├── bot_service/
│   ├── app/
│   ├── tests/
│   ├── .env
│   ├── pyproject.toml
│   └── pytest.ini
├── docker-compose.yml
└── README.md
```
## Архитектура проекта
- **Auth Service**: регистрация, логин, выдача JWT
- **Bot Service**: Telegram bot + Celery + RabbitMQ + Redis
- LLM запросы уходят в очередь, обрабатываются воркером

## Запуск
docker-compose up --build