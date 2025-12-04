# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ...utilities import db
from ..user.service import get_user_by_id
from ..post.service import get_post_by_id, update_post
from .model import Comment
from .schemas import CommentCreate, CommentResponse, CommentUpdate


# Get the comments collection
comments_collection: AsyncIOMotorCollection = db["comments"]


async def create_comment(comment_data: CommentCreate) -> Comment:
    """Create a new comment."""
    # Check if user exists
    user = await get_user_by_id(comment_data.user_id)
    if not user:
        raise ValueError("User not found")

    # Check if post exists
    post = await get_post_by_id(comment_data.post_id)
    if not post:
        raise ValueError("Post not found")

    # Check if post already has a comment (one-to-one)
    if post.comment_id is not None:
        raise ValueError("Post already has a comment")

    # Convert ids to ObjectId
    try:
        user_id_obj = ObjectId(comment_data.user_id)
        post_id_obj = ObjectId(comment_data.post_id)
    except:
        raise ValueError("Invalid user_id or post_id")

    # Create comment document
    comment_doc = {
        "user_id": user_id_obj,
        "title": comment_data.title,
        "post_id": post_id_obj,
        "created_at": datetime.utcnow()
    }

    # Insert into database
    result = await comments_collection.insert_one(comment_doc)
    comment_doc["_id"] = result.inserted_id
    comment_id = result.inserted_id

    # Update post with comment_id
    from ..post.schemas import PostUpdate
    await update_post(comment_data.post_id, PostUpdate(title=None, comment_id=str(comment_id)))

    # Return Comment model
    return Comment(**comment_doc)


async def get_comment_by_id(comment_id: str) -> Optional[Comment]:
    """Get comment by ID."""
    try:
        obj_id = ObjectId(comment_id)
    except:
        return None

    comment_doc = await comments_collection.find_one({"_id": obj_id})
    if comment_doc:
        return Comment(**comment_doc)
    return None


async def get_comment_by_post_id(post_id: str) -> Optional[Comment]:
    """Get comment by post ID (one-to-one)."""
    try:
        post_id_obj = ObjectId(post_id)
    except:
        return None

    comment_doc = await comments_collection.find_one({"post_id": post_id_obj})
    if comment_doc:
        return Comment(**comment_doc)
    return None


async def get_comments_by_user(user_id: str) -> List[Comment]:
    """Get all comments by a user."""
    try:
        user_id_obj = ObjectId(user_id)
    except:
        return []

    comments_docs = await comments_collection.find({"user_id": user_id_obj}).to_list(length=None)
    return [Comment(**doc) for doc in comments_docs]


async def update_comment(comment_id: str, update_data: CommentUpdate) -> Optional[Comment]:
    """Update comment information."""
    try:
        obj_id = ObjectId(comment_id)
    except:
        return None

    update_dict = {}
    if update_data.title is not None:
        update_dict["title"] = update_data.title

    if update_dict:
        result = await comments_collection.update_one(
            {"_id": obj_id},
            {"$set": update_dict}
        )
        if result.modified_count > 0:
            return await get_comment_by_id(comment_id)
    return None


async def delete_comment(comment_id: str) -> bool:
    """Delete comment by ID."""
    try:
        obj_id = ObjectId(comment_id)
    except:
        return False

    # Get comment to find post_id
    comment = await get_comment_by_id(comment_id)
    if not comment:
        return False

    # Delete comment
    result = await comments_collection.delete_one({"_id": obj_id})
    if result.deleted_count > 0:
        # Update post to remove comment_id
        from ..post.schemas import PostUpdate
        await update_post(str(comment.post_id), PostUpdate(title=None, comment_id=None))
        return True
    return False


async def get_all_comments() -> List[Comment]:
    """Get all comments."""
    comments_docs = await comments_collection.find().to_list(length=None)
    return [Comment(**doc) for doc in comments_docs]


__all__ = [
    "create_comment",
    "get_comment_by_id",
    "get_comment_by_post_id",
    "get_comments_by_user",
    "update_comment",
    "delete_comment",
    "get_all_comments",
]