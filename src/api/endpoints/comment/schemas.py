# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    user_id: str  # Will convert to ObjectId
    title: str = Field(..., min_length=1, max_length=500)
    post_id: str  # Will convert to ObjectId


class CommentResponse(BaseModel):
    id: str
    user_id: str
    title: str
    post_id: str
    created_at: datetime


class CommentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)


__all__ = ["CommentCreate", "CommentResponse", "CommentUpdate"]