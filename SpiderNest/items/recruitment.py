"""
author: thomaszdxsn
"""
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst

from .processors import created_time_input_processor


class RecruitmentItem(Item):
    title = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    job_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    company_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    publish_time = Field(
        input_processor=MapCompose(str.strip, created_time_input_processor),
        output_processor=TakeFirst()
    )