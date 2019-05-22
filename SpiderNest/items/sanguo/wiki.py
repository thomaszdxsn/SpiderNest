"""
author: thomaszdxsn
"""
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join, MapCompose

__all__ = ("SanguoWikiCharacterItem",)


class SanguoWikiCharacterItem(Item):
    _img_fields = ['image']
    name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    image = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Join()
    )
    source = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
