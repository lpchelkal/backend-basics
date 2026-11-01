from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "заказы кофе"
    default_page_size: int = 10
    max_page_size: int = 50
    model_config: SettingsConfigDict = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()