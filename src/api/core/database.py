# -*- coding: utf-8 -*-
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    """Application settings from environment variables."""

    mongodb_url: str = "mongodb://admin:admin123@localhost:27017"
    database_name: str = "mydb"
    password_pepper: SecretStr = SecretStr("your_super_secret_pepper_key_change_this_in_production")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra='ignore'
    )


settings = Settings()

# Create MongoDB client
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_url)

# Get database
db: AsyncIOMotorDatabase = client[settings.database_name]


__all__ = [
    "client",
    "db",
    "settings",
]