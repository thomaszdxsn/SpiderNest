"""
author: thomaszdxsn
"""
from scrapy.item import Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from ..post import PostItem
from ..estate import EstateItem, EstateType
from ...core.mixin import item_default_val_mixin_factory

__all__ = ("LyEstatePostItem", 'LyEstateNewItem', 'LyEstateSecondItem', "LyEstateRentItem")


class LyEstatePostItem(PostItem):
    content = Field(
        output_processor=Join()
    )
    brief = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )


class LyEstateNewItem(item_default_val_mixin_factory(type=EstateType.NEW.value), EstateItem):
    pass


class LyEstateSecondItem(item_default_val_mixin_factory(type=EstateType.SECOND_HAND.value), EstateItem):
    pass


class LyEstateRentItem(item_default_val_mixin_factory(type=EstateType.RENT.value), EstateItem):
    pass