# -*- coding: utf-8 -*-
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    mongodb_url: str
    database_name: str
    

    password_pepper: SecretStr
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()

# Create MongoDB client
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_url)

# Get database
database: AsyncIOMotorDatabase = client[settings.database_name]


__all__ = [
    "client",
    "database",
    "settings",
]