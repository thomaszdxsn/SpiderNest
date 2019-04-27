"""
author: thomaszdxsn
"""
from enum import Enum

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Identity

__all__ = ('EstateItem',)

class EstateType(Enum):
    NEW = 'NEW'
    SECOND_HAND = 'SECOND_HAND'
    RENT = 'RENT'


class EstateItem(Item):
    name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    tags = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Identity()
    )
    type = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )