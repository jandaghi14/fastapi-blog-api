from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()


class Settings_JWT(BaseSettings):
    JWT_DEFAULT_TIME_EXPIRE: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    class Config:
        env_file = ".env"


settings_jwt = Settings_JWT()
