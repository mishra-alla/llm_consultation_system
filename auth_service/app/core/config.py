from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "auth-service"
    env: str = "local"

    jwt_secret: str
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 60

    sqlite_path: str = "./auth.db"

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.sqlite_path}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
