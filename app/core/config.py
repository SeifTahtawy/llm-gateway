from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )

    app_name: str = "LLM Gateway"
    app_version: str = "0.1.0"
    app_description: str = "A gateway for LLMs"
    debug: bool = False
    google_api_key: SecretStr | None = None


settings = AppSettings()
