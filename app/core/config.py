from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Application settings."""

    app_name: str = "LLM Gateway"
    app_version: str = "0.1.0"
    app_description: str = "A gateway for LLMs"
    debug: bool = False


settings = AppSettings()
