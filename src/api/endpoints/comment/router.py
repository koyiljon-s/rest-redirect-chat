# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, HTTPException, status

from .schemas import CommentCreate, CommentResponse, CommentUpdate
from .service import (
    create_comment,
    get_comment_by_id,
    get_comment_by_post_id,
    get_comments_by_user,
    update_comment,
    delete_comment,
    get_all_comments
)


router = APIRouter()


@router.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment_endpoint(comment: CommentCreate) -> CommentResponse:
    """Create a new comment."""
    try:
        comment_obj = await create_comment(comment)
        return CommentResponse(
            id=str(comment_obj.id),
            user_id=str(comment_obj.user_id),
            title=comment_obj.title,
            post_id=str(comment_obj.post_id),
            created_at=comment_obj.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/comments/{comment_id}", response_model=CommentResponse)
async def get_comment_endpoint(comment_id: str) -> CommentResponse:
    """Get comment by ID."""
    comment = await get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return CommentResponse(
        id=str(comment.id),
        user_id=str(comment.user_id),
        title=comment.title,
        post_id=str(comment.post_id),
        created_at=comment.created_at
    )


@router.get("/posts/{post_id}/comment", response_model=CommentResponse)
async def get_comment_by_post_endpoint(post_id: str) -> CommentResponse:
    """Get comment by post ID."""
    comment = await get_comment_by_post_id(post_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return CommentResponse(
        id=str(comment.id),
        user_id=str(comment.user_id),
        title=comment.title,
        post_id=str(comment.post_id),
        created_at=comment.created_at
    )


@router.get("/comments", response_model=List[CommentResponse])
async def get_all_comments_endpoint() -> List[CommentResponse]:
    """Get all comments."""
    comments = await get_all_comments()
    return [
        CommentResponse(
            id=str(comment.id),
            user_id=str(comment.user_id),
            title=comment.title,
            post_id=str(comment.post_id),
            created_at=comment.created_at
        )
        for comment in comments
    ]


@router.get("/users/{user_id}/comments", response_model=List[CommentResponse])
async def get_comments_by_user_endpoint(user_id: str) -> List[CommentResponse]:
    """Get all comments by a user."""
    comments = await get_comments_by_user(user_id)
    return [
        CommentResponse(
            id=str(comment.id),
            user_id=str(comment.user_id),
            title=comment.title,
            post_id=str(comment.post_id),
            created_at=comment.created_at
        )
        for comment in comments
    ]


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment_endpoint(comment_id: str, comment_update: CommentUpdate) -> CommentResponse:
    """Update comment information."""
    comment = await update_comment(comment_id, comment_update)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return CommentResponse(
        id=str(comment.id),
        user_id=str(comment.user_id),
        title=comment.title,
        post_id=str(comment.post_id),
        created_at=comment.created_at
    )


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_endpoint(comment_id: str):
    """Delete comment by ID."""
    deleted = await delete_comment(comment_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")


__all__ = ["router"]