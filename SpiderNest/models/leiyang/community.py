"""
author: thomaszdxsn
"""
from datetime import datetime

from pydantic import BaseModel

__all__ = ('LyCommunityPost',)


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