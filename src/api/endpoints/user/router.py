# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException, status

from .schemas import UserCreate, UserResponse, UserUpdate
from .service import create_user, get_user_by_id, update_user, delete_user


router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate) -> UserResponse:
    """Create a new user."""
    try:
        user_obj = await create_user(user)
        return UserResponse(
            id=str(user_obj.id),
            username=user_obj.username,
            email=user_obj.email,
            created_at=user_obj.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: str) -> UserResponse:
    """Get user by ID."""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: str, user_update: UserUpdate) -> UserResponse:
    """Update user information."""
    user = await update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(user_id: str):
    """Delete user by ID."""
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


__all__ = ["router"]