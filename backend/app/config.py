from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DevInsight API"
    environment: str = "development"
    database_url: str = "sqlite:///./devinsight.db"
    github_client_id: str = ""
    github_client_secret: str = ""
    secret_key: str = "replace-me-in-development"
    redis_url: str = "redis://localhost:6379/0"
    frontend_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
