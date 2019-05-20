"""
author: thomaszdxsn
"""
from scrapy import Item, Field

__all__ = ("SanguoWikiCharacterItem",)


class SanguoWikiCharacterItem(Item):
    name = Field()
    image = Field()
    description = Field()
    source = Field()
