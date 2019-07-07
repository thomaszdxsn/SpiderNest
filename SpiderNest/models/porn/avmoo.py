from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

__all__ = ('AvmooActress', "AvmooMovie")


class AvmooActress(BaseModel):
    name_cn: str
    name_en: str
    name_jp: str
    info: dict
    avatar: str


class AvmooMovie(BaseModel):
    title: str
    code: str
    publish_time: datetime
    time_length: str
    publish_vendor: str
    create_vendor: str
    categories: List[str]
    cast: List[str]
    cover: str
    stills: Optional[List[str]]
    director: Optional[str]
