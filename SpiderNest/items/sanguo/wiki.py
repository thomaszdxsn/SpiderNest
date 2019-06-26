"""
author: thomaszdxsn
"""
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join, MapCompose

from ..image import register_image_fields

__all__ = ("SanguoWikiCharacterItem",)


@register_image_fields('image')
class SanguoWikiCharacterItem(Item):
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
