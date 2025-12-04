# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ...utilities import db
from ..user.service import get_user_by_id
from .model import Post
from .schemas import PostCreate, PostResponse, PostUpdate


# Get the posts collection
posts_collection: AsyncIOMotorCollection = db["posts"]


async def create_post(post_data: PostCreate) -> Post:
    """Create a new post."""
    # Check if user exists
    user = await get_user_by_id(post_data.user_id)
    if not user:
        raise ValueError("User not found")

    # Convert user_id to ObjectId
    try:
        user_id_obj = ObjectId(post_data.user_id)
    except:
        raise ValueError("Invalid user_id")

    # Convert comment_id if provided
    comment_id_obj = None
    if post_data.comment_id:
        try:
            comment_id_obj = ObjectId(post_data.comment_id)
        except:
            raise ValueError("Invalid comment_id")

    # Create post document
    post_doc = {
        "user_id": user_id_obj,
        "title": post_data.title,
        "upvotes": 0,
        "downvotes": 0,
        "created_at": datetime.utcnow(),
        "comment_id": comment_id_obj
    }

    # Insert into database
    result = await posts_collection.insert_one(post_doc)
    post_doc["_id"] = result.inserted_id

    # Return Post model
    return Post(**post_doc)


async def get_post_by_id(post_id: str) -> Optional[Post]:
    """Get post by ID."""
    try:
        obj_id = ObjectId(post_id)
    except:
        return None

    post_doc = await posts_collection.find_one({"_id": obj_id})
    if post_doc:
        return Post(**post_doc)
    return None


async def get_posts_by_user(user_id: str) -> List[Post]:
    """Get all posts by a user."""
    try:
        user_id_obj = ObjectId(user_id)
    except:
        return []

    posts_docs = await posts_collection.find({"user_id": user_id_obj}).to_list(length=None)
    return [Post(**doc) for doc in posts_docs]


async def update_post(post_id: str, update_data: PostUpdate) -> Optional[Post]:
    """Update post information."""
    try:
        obj_id = ObjectId(post_id)
    except:
        return None

    update_dict = {}
    if update_data.title is not None:
        update_dict["title"] = update_data.title
    if update_data.upvotes is not None:
        update_dict["upvotes"] = update_data.upvotes
    if update_data.downvotes is not None:
        update_dict["downvotes"] = update_data.downvotes
    if update_data.comment_id is not None:
        if update_data.comment_id:
            try:
                update_dict["comment_id"] = ObjectId(update_data.comment_id)
            except:
                raise ValueError("Invalid comment_id")
        else:
            update_dict["comment_id"] = None

    if update_dict:
        result = await posts_collection.update_one(
            {"_id": obj_id},
            {"$set": update_dict}
        )
        if result.modified_count > 0:
            return await get_post_by_id(post_id)
    return None


async def delete_post(post_id: str) -> bool:
    """Delete post by ID."""
    try:
        obj_id = ObjectId(post_id)
    except:
        return False

    result = await posts_collection.delete_one({"_id": obj_id})
    return result.deleted_count > 0


async def get_all_posts() -> List[Post]:
    """Get all posts."""
    posts_docs = await posts_collection.find().to_list(length=None)
    return [Post(**doc) for doc in posts_docs]


__all__ = [
    "create_post",
    "get_post_by_id",
    "get_posts_by_user",
    "update_post",
    "delete_post",
    "get_all_posts",
]