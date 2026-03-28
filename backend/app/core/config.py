from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Autonomous Equity Analyst"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/tinyfish26"
    openai_api_key: str = ""
    tinyfish_api_key: str = ""
    tinyfish_base_url: str = "https://agent.tinyfish.ai/v1"
    scheduler_minutes: int = 60
    enabled_tickers: list[str] = ["NVDA"]
    tinyfish_proxy_country_code: str = "US"
    tinyfish_browser_profile: str = "lite"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
