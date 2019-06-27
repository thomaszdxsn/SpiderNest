"""
author: thomaszdxsn
"""
from pydantic import BaseModel

__all__ = ('XArtModel',)


class XArtModel(BaseModel):
    name: str
    photo: str
    brief: str
    age: int
    country: str
    vote_count: int
    vote_score: float