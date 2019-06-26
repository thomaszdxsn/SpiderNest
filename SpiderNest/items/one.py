"""
author: thomaszdxsn
"""
from datetime import datetime

import arrow
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join, MapCompose, Compose

from .image import register_image_fields

__all__ = ('OneImgItem',)


def revert_date(d_str: str) -> datetime:
    fmt = ['DDMMM YYYY', 'DMMM YYYY']
    return arrow.get(d_str, fmt).naive


@register_image_fields('image')
class OneImgItem(Item):
    image = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    title = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    proverb = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    date = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Compose(Join(''),  str.strip, revert_date)
    )