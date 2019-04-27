"""
author: thomaszdxsn
"""
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose

from .processors import populate_abs_url, created_time_input_processor


class PostItem(Item):
    title = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    url = Field(
        input_processor=MapCompose(str, str.strip, populate_abs_url),
        output_processor=TakeFirst()
    )
    author = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    view_count = Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    created_time = Field(
        input_processor=MapCompose(str.strip, created_time_input_processor),
        output_processor=TakeFirst()
    )
    content = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )