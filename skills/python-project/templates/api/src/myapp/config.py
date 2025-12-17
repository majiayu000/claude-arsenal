"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "myapp"
    debug: bool = False
    port: int = 8000

    # Database
    database_url: str = "postgresql+asyncpg://localhost/myapp"

    # LiteLLM
    litellm_url: str = "http://localhost:4000"
    litellm_api_key: str = ""
    default_model: str = "gpt-4o"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
