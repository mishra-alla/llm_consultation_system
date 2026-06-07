from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "bot-service"
    env: str = "local"

    # Telegram
    telegram_bot_token: str

    # JWT
    jwt_secret: str
    jwt_alg: str = "HS256"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672//"

    # OpenRouter
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openai/gpt-3.5-turbo"
    openrouter_site_url: str = "https://example.com"
    openrouter_app_name: str = "bot-service"

    # # Proxy settings 
    # proxy_url: str | None = None
    # proxy_password: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
