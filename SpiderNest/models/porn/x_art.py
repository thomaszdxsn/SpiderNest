"""
author: thomaszdxsn
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

__all__ = ('XArtModel', 'XArtVideo', "XArtBlogPost")


class XArtModel(BaseModel):
    name: str
    photo: str
    brief: str
    age: Optional[int]
    country: str
    vote_count: int
    vote_score: float


class XArtVideo(BaseModel):
    name: str
    cover: str
    screenshots: List[str]
    publish_time: datetime
    brief: str
    cast: Optional[List[str]]
    vote_count: int
    vote_score: float


class XArtBlogPost(BaseModel):
    title: str
    like_count: int
    publish_time: datetime
    content: str