"""
author: thomaszdxsn
"""
from typing import Optional

from pydantic import BaseModel

__all__ = ('IP',)


class IP(BaseModel):
    ip: str
    port: str
    protocol: str
    remark: Optional[str]
    source: str