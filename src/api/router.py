# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .endpoints.user.router import router as user_router
from .endpoints.post.router import router as post_router
from .endpoints.comment.router import router as comment_router


router = APIRouter()

# Include user endpoints
router.include_router(user_router, prefix="/api", tags=["users"])

# Include post endpoints
router.include_router(post_router, prefix="/api", tags=["posts"])

# Include comment endpoints
router.include_router(comment_router, prefix="/api", tags=["comments"])


__all__ = ["router"]