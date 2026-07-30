"""
Application configuration.

Loads all runtime configuration from environment variables using
pydantic-settings. A single `settings` object is imported wherever
configuration values are needed, keeping environment access in one place.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings, populated from environment variables."""

    # --- Database ---
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/video_generator"
    )

    # --- Replicate AI Provider ---
    REPLICATE_API_TOKEN: str = ""

    # --- App behavior ---
    MAX_HISTORY_RECORDS: int = 5
    GENERATION_TIMEOUT_SECONDS: int = 300
    APP_NAME: str = "AI Video Generator"
    CORS_ORIGINS: str = (
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()