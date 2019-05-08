"""
author: thomaszdxsn
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

__all__ = ('LyRencaiJobInfo',)


class LyRencaiJobInfo(BaseModel):
    title: str
    company_name: str
    salary: Optional[List[int]]
    requirements: Optional[List[str]]
    tags: Optional[List[str]]
    publish_time: datetime
    description: Optional[str]


class LyRencaiCompanyInfo(BaseModel):
    name: str
    cover: str
    tags: List[str]
    description: Optional[str]