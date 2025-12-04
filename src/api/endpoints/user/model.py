# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    username: str
    email: str
    password: str  # hashed password
    password_salt: str
    created_at: datetime

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


__all__ = ["User"]