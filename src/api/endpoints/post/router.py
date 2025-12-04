# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, HTTPException, status

from .schemas import PostCreate, PostResponse, PostUpdate
from .service import create_post, get_post_by_id, get_posts_by_user, update_post, delete_post, get_all_posts


router = APIRouter()


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post_endpoint(post: PostCreate) -> PostResponse:
    """Create a new post."""
    try:
        post_obj = await create_post(post)
        return PostResponse(
            id=str(post_obj.id),
            user_id=str(post_obj.user_id),
            title=post_obj.title,
            upvotes=post_obj.upvotes,
            downvotes=post_obj.downvotes,
            created_at=post_obj.created_at,
            comment_id=str(post_obj.comment_id) if post_obj.comment_id else None
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_endpoint(post_id: str) -> PostResponse:
    """Get post by ID."""
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return PostResponse(
        id=str(post.id),
        user_id=str(post.user_id),
        title=post.title,
        upvotes=post.upvotes,
        downvotes=post.downvotes,
        created_at=post.created_at,
        comment_id=str(post.comment_id) if post.comment_id else None
    )


@router.get("/posts", response_model=List[PostResponse])
async def get_all_posts_endpoint() -> List[PostResponse]:
    """Get all posts."""
    posts = await get_all_posts()
    return [
        PostResponse(
            id=str(post.id),
            user_id=str(post.user_id),
            title=post.title,
            upvotes=post.upvotes,
            downvotes=post.downvotes,
            created_at=post.created_at,
            comment_id=str(post.comment_id) if post.comment_id else None
        )
        for post in posts
    ]


@router.get("/users/{user_id}/posts", response_model=List[PostResponse])
async def get_posts_by_user_endpoint(user_id: str) -> List[PostResponse]:
    """Get all posts by a user."""
    posts = await get_posts_by_user(user_id)
    return [
        PostResponse(
            id=str(post.id),
            user_id=str(post.user_id),
            title=post.title,
            upvotes=post.upvotes,
            downvotes=post.downvotes,
            created_at=post.created_at,
            comment_id=str(post.comment_id) if post.comment_id else None
        )
        for post in posts
    ]


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post_endpoint(post_id: str, post_update: PostUpdate) -> PostResponse:
    """Update post information."""
    try:
        post = await update_post(post_id, post_update)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return PostResponse(
            id=str(post.id),
            user_id=str(post.user_id),
            title=post.title,
            upvotes=post.upvotes,
            downvotes=post.downvotes,
            created_at=post.created_at,
            comment_id=str(post.comment_id) if post.comment_id else None
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_endpoint(post_id: str):
    """Delete post by ID."""
    deleted = await delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


__all__ = ["router"]