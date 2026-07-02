from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore",
)


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_DOMAIN: str

    model_config = _base_config


class RedisConfig(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    model_config = _base_config

    def REDIS_URL(self, db):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"


app_settings = AppSettings()
redis_settings = RedisConfig()
