from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose

__all__ = ("AvmooActressItem", "AvmooMovieItem")


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


class AvmooMovieItem(Item):
    title = Field()
    code = Field()
    publish_time = Field()
    time_length = Field()
    publish_vendor = Field()
    create_vendor = Field()
    categories = Field()
    cast = Field()
    cover = Field()
    stills = Field()
    director = Field()
