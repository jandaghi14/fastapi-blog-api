from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra='ignore')

    DATABASE_URL: str
    TEST_DATABASE_URL: str


settings = Settings()


class Settings_JWT(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra='ignore')

    JWT_DEFAULT_TIME_EXPIRE: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str


settings_jwt = Settings_JWT()
