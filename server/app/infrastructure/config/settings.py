from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://app:change-me@127.0.0.1:3306/a_stock_platform"
    port: int = 3000
    tushare_token: str | None = None
    task_admin_token: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
