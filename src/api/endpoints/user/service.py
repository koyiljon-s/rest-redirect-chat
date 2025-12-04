# -*- coding: utf-8 -*-
import secrets
from datetime import datetime
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from pydantic import SecretStr

from ...utilities import async_hash, db, settings
from .model import User
from .schemas import UserCreate, UserResponse, UserUpdate


# Get the users collection
users_collection: AsyncIOMotorCollection = db["users"]


async def create_user(user_data: UserCreate) -> User:
    """Create a new user."""
    # Check if username or email already exists
    existing_user = await users_collection.find_one({
        "$or": [
            {"username": user_data.username},
            {"email": user_data.email}
        ]
    })
    if existing_user:
        raise ValueError("Username or email already exists")

    # Generate salt
    password_salt = secrets.token_hex(16)

    # Hash password
    hashed_password = await async_hash(
        user_data.password,
        SecretStr(password_salt),
        settings.password_pepper
    )

    # Create user document
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password,
        "password_salt": password_salt,
        "created_at": datetime.utcnow()
    }

    # Insert into database
    result = await users_collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    # Return User model
    return User(**user_doc)


async def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID."""
    try:
        obj_id = ObjectId(user_id)
    except:
        return None

    user_doc = await users_collection.find_one({"_id": obj_id})
    if user_doc:
        return User(**user_doc)
    return None


async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    user_doc = await users_collection.find_one({"email": email})
    if user_doc:
        return User(**user_doc)
    return None


async def update_user(user_id: str, update_data: UserUpdate) -> Optional[User]:
    """Update user information."""
    try:
        obj_id = ObjectId(user_id)
    except:
        return None

    update_dict = {}
    if update_data.username:
        update_dict["username"] = update_data.username
    if update_data.email:
        update_dict["email"] = update_data.email
    if update_data.password:
        # Generate new salt and hash
        password_salt = secrets.token_hex(16)
        hashed_password = await async_hash(
            update_data.password,
            SecretStr(password_salt),
            settings.password_pepper
        )
        update_dict["password"] = hashed_password
        update_dict["password_salt"] = password_salt

    if update_dict:
        result = await users_collection.update_one(
            {"_id": obj_id},
            {"$set": update_dict}
        )
        if result.modified_count > 0:
            return await get_user_by_id(user_id)
    return None


async def delete_user(user_id: str) -> bool:
    """Delete user by ID."""
    try:
        obj_id = ObjectId(user_id)
    except:
        return False

    result = await users_collection.delete_one({"_id": obj_id})
    return result.deleted_count > 0


__all__ = [
    "create_user",
    "get_user_by_id",
    "get_user_by_email",
    "update_user",
    "delete_user",
]