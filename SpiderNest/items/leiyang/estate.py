"""
author: thomaszdxsn
"""
from scrapy.item import Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity, Compose

from ..post import PostItem
from ..estate import EstateItem, EstateType
from ..processors import convert_to_float, convert_num_with_unit
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
    tags = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Identity()
    )
    price_per_square = Field(
        input_processor=MapCompose(convert_to_float),
        output_processor=TakeFirst()
    )
    main_styles = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    developer = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    project_type = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    decoration = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    address = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    marketing_address = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )


class LyEstateSecondItem(item_default_val_mixin_factory(type=EstateType.SECOND_HAND.value), EstateItem):
    price = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Compose(Join(separator=''), convert_num_with_unit)
    )
    area = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    style = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    direction = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    floor = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    house_type = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    decoration = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    age = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    address = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join()
    )
    images = Field(
        input_processor=MapCompose(str.strip, lambda x: 'https:' + x),
        output_processor=Identity()
    )


class LyEstateRentItem(item_default_val_mixin_factory(type=EstateType.RENT.value), EstateItem):
    per_month_price = Field(
        input_processor=MapCompose(str.strip, convert_to_float),
        output_processor=TakeFirst()
    )
    area = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    style = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    direction = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    floor = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    house_type = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    decoration = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    age = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    address = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join()
    )
    images = Field(
        input_processor=MapCompose(str.strip, lambda x: 'https:' + x),
        output_processor=Identity()
    )