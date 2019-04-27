"""
author: thomaszdxsn
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

__all__ = ('LyEstatePost', "LyEstateNewInfo", "LyEstateSecondHandInfo", "LyEstateRentInfo")


class LyEstatePost(BaseModel):
    author: str
    content: str
    brief: str
    created_time: datetime
    url: str
    view_count: int


class LyEstateNewInfo(BaseModel):
    title: str
    type: str
    description: str
    developer: str
    address: str
    marketing_address: str
    price_per_square: float
    project_type: str
    tags: List[str]
    main_styles: str


class LyEstateSecondHandInfo(BaseModel):
    title: str
    type: str
    price: float
    area: float
    style: Optional[str]
    direction: Optional[str]
    floor: Optional[str]
    house_type: Optional[str]
    decoration: Optional[str]
    age: Optional[str]
    address: Optional[str]
    description: Optional[str]
    images: Optional[List[str]]


class LyEstateRentInfo(BaseModel):
    title: str
    type: str
    per_month_price: float
    area: float
    style: Optional[str]
    direction: Optional[str]
    floor: Optional[str]
    house_type: Optional[str]
    decoration: Optional[str]
    age: Optional[str]
    address: Optional[str]
    description: Optional[str]
    images: Optional[List[str]]