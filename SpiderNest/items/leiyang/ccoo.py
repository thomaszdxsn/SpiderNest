"""
author: thomaszdxsn
"""
from typing import List, Any

from scrapy import Field
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from ..recruitment import RecruitmentItem
from ..processors import replace_cn_punc

__all__ = ('LyCcooRecruitmentItem',)


def _index_list_val(lst: list, index: int, default: Any=None) -> Any:
    try:
        return lst[index]
    except IndexError:
        return default


def construct_info(info_strs: List[str]) -> dict:
    info_strs = [s for s in info_strs if s]
    return dict(
        (s, _index_list_val(info_strs, i + 1, default='--'))
        for i, s in enumerate(info_strs)
        if i % 2 == 0
    )


class LyCcooRecruitmentItem(RecruitmentItem):
    company_info = Field(
        input_processor=MapCompose(str.strip, replace_cn_punc),
        output_processor=construct_info
    )
    company_description = Field(
        output_processor=Join()
    )
    job_info = Field(
        input_processor=MapCompose(str.strip, replace_cn_punc),
        output_processor=construct_info
    )
    job_description = Field(
        output_processor=TakeFirst()
    )
