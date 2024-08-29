from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения.
    Использует Pydantic для валидации переменных окружения.
    """
    app_name: str
    environment: str
    mongodb_url: str
    mongodb_name: str
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
