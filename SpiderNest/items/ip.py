"""
author: thomaszdxsn
"""
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join

__all__ = ("IPItem",)


class IPItem(scrapy.Item):
    ip = scrapy.Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    port = scrapy.Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    protocol = scrapy.Field(
        input_processor=MapCompose(str, str.strip, str.lower),
        output_processor=TakeFirst()
    )
    remark = scrapy.Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Join(separator=', ')
    )
    source = scrapy.Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )