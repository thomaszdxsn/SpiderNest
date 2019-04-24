"""
author: thomaszdxsn
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

__all__ = ('LyCommunityPost', 'LyCommunityUser', 'LyCommunityComment')


class LyCommunityPost(BaseModel):
    block_name: str
    title: str
    url: str
    author_username: str
    view_count: int
    comment_count: int
    has_attachment: bool
    has_image: bool
    created_time: datetime
    last_comment_time: datetime
    last_comment_username: str


class LyCommunityUser(BaseModel):
    username: str
    avatar_url: str
    topic_count: int
    post_count: int
    credit_count: int
    coin_count: int
    medal_list: List[str]
    signature: Optional[str]
    user_group: str


class LyCommunityComment(BaseModel):
    post_url: str
    author_username: str
    floor: int
    created_time: datetime
    content: str
    signature: Optional[str]
    image_urls: Optional[List[str]]