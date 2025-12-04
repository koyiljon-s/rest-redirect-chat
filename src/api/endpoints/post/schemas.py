# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    user_id: str  # Will convert to ObjectId
    title: str = Field(..., min_length=1, max_length=200)
    comment_id: Optional[str] = None


class PostResponse(BaseModel):
    id: str
    user_id: str
    title: str
    upvotes: int
    downvotes: int
    created_at: datetime
    comment_id: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    upvotes: Optional[int] = None
    downvotes: Optional[int] = None
    comment_id: Optional[str] = None


__all__ = ["PostCreate", "PostResponse", "PostUpdate"]