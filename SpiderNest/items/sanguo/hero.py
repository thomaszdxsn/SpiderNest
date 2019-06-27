"""
author: thomaszdxsn
"""
from scrapy import Item, Field

from ..image import register_image_fields

__all__ = ("SanguoOlHeroItem",)


@register_image_fields('pic')
class SanguoOlHeroItem(Item):
    name = Field()
    name_pinyin = Field()
    name_zi = Field()
    life_range = Field()
    come_from = Field()
    brief = Field()
    cata = Field()
    pic = Field()
    sex = Field()