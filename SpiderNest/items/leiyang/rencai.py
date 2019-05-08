"""
author: thomaszdxsn
"""
import re
from typing import Optional, List

from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, Join, Identity, TakeFirst

from ..recruitment import RecruitmentItem

__all__ = ('LyRencaiRecruitmentItem', 'LyRencaiCompanyItem')


def salary_input_processor(val: str) -> Optional[List[int]]:
    digit_match = list(re.findall(r'(\d+)', val))
    if any(i is None for i in digit_match):
        return
    return [int(i) for i in digit_match]


def salary_output_processor(val: List[Optional[list]]) -> Optional[List[int]]:
    return [v for v in val if isinstance(v, int)]



class LyRencaiRecruitmentItem(RecruitmentItem):
    # salary是一个2-item数组，包含工资范围。但是有可能为空
    salary = Field(
        input_processor=MapCompose(salary_input_processor),
        output_processor=salary_output_processor
    )
    requirements = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Identity()
    )
    tags = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Identity()
    )
    description = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Join('')
    )


class LyRencaiCompanyItem(Item):
    name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    cover = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    tags = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Identity()
    )
    description = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Join()
    )