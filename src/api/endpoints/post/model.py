# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Post(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    user_id: ObjectId
    title: str
    upvotes: int = 0
    downvotes: int = 0
    created_at: datetime
    comment_id: Optional[ObjectId] = None

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


__all__ = ["Post"]