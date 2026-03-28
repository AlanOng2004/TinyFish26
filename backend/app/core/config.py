from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Autonomous Equity Analyst"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/tinyfish26"
    cors_origins: list[str] = ["http://localhost:5173", "https://stocks.thealan.net"]
    openai_api_key: str = ""
    tinyfish_api_key: str = ""
    tinyfish_base_url: str = "https://agent.tinyfish.ai/v1"
    scheduler_minutes: int = 60
    enabled_tickers: list[str] = ["NVDA"]
    tinyfish_enabled_sources: list[str] = ["yahoo_quote", "google_finance_news"]
    tinyfish_proxy_country_code: str = "US"
    tinyfish_browser_profile: str = "lite"
    tinyfish_request_timeout_seconds: int = 45

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
