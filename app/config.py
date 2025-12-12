# app/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://root:example@localhost:27017"
    MASTER_DB: str = "master_db"
    JWT_SECRET: str = "super-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SALT_ROUNDS: int = 12  # passlib/bcrypt rounds (bcrypt chooses automatically)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
