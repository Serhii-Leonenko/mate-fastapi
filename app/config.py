from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "API"
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
