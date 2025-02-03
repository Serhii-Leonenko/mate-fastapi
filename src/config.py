import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "API"
    DATABASE_URL: str = os.environ["DATABASE_URL"]

    class Config:
        env_file = ".env"


settings = Settings()
