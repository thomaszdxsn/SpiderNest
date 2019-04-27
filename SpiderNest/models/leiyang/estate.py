"""
author: thomaszdxsn
"""
from datetime import datetime

from pydantic import BaseModel

__all__ = ('LyEstatePost',)


class LyEstatePost(BaseModel):
    author: str
    content: str
    brief: str
    created_time: datetime
    url: str
    view_count: int