from functools import lru_cache

from pydantic import model_validator
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
    github_redirect_uri: str = "http://localhost:8000/auth/github/callback"
    github_scope: str = "read:user user:email repo"
    session_max_age: int = 3600

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def validate_production_security(self):
        if self.environment == "production":
            if self.secret_key in {"replace-me-in-development", "local-development-only"} or len(self.secret_key) < 32:
                raise ValueError("SECRET_KEY must be a random value of at least 32 characters in production")
            if not self.frontend_url.startswith("https://") or not self.github_redirect_uri.startswith("https://"):
                raise ValueError("Production frontend and OAuth redirect URLs must use HTTPS")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
