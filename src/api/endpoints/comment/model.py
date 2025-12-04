# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Comment(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    user_id: ObjectId
    title: str
    post_id: ObjectId
    created_at: datetime

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


__all__ = ["Comment"]