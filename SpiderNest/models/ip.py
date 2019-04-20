"""
author: thomaszdxsn
"""
from pydantic import BaseModel

__all__ = ('IP',)


class IP(BaseModel):
    ip: str
    port: str
    protocol: str
    remark: str
    source: str