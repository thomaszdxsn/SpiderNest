import arrow
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Identity

from ..image import register_image_fields

__all__ = ("AvmooActressItem", "AvmooMovieItem")


@register_image_fields('avatar')
class AvmooActressItem(Item):
    name_cn = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    name_jp = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    name_en = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    info = Field(
        input_processor=lambda x: [i.split(':') for i in x],
        output_processor=lambda x: {k.strip(): v.strip() for k, v in x}
    )
    avatar = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )


@register_image_fields('cover', 'stills')
class AvmooMovieItem(Item):
    title = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    code = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    publish_time = Field(
        input_processor=MapCompose(arrow.get, lambda x: x.naive),
        output_processor=TakeFirst()
    )
    time_length = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    publish_vendor = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    create_vendor = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    categories = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Identity()
    )
    cast = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Identity()
    )
    cover = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    stills = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Identity()
    )
    director = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
