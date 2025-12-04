# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: SecretStr = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = Field(None, min_length=8)


__all__ = ["UserCreate", "UserResponse", "UserUpdate"]