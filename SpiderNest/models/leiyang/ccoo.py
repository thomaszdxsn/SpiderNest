"""
author: thomaszdxsn
"""
from typing import Optional

from pydantic import BaseModel


class LyCcooRecruitmentInfo(BaseModel):
    title: str
    job_name: str
    job_info: dict
    job_description: Optional[str]
    company_name: str
    company_info: dict
    company_description: Optional[str]