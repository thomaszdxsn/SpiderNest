"""
author: thomaszdxsn
"""
from typing import Optional

from pydantic import BaseModel


class SanguoWikiCharacter(BaseModel):
    name: str
    image: str
    description: str
    source: Optional[str]