"""
author: thomaszdxsn
"""
import re
from datetime import datetime
from typing import Optional

from scrapy import Field, Item
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join

from ..image import register_image_fields

__all__ = ("XArtModelItem", "XArtVideoItem", "XArtBlogPostItem")

VOTE_SCORE_PATTERN = re.compile(r'([\d.]+) / 10')
VOTE_COUNT_PATTERN = re.compile(r'\((\d+) votes\)')


def extract_vote_score(val: str) -> str:
    return VOTE_SCORE_PATTERN.search(val).group(1)


def extract_vote_count(val: str) -> str:
    return VOTE_COUNT_PATTERN.search(val).group(1)


def intfy(s: str) -> Optional[int]:
    if s != '':
        return int(s)


def convert_datetime(s: str) -> datetime:
    return datetime.strptime(s, '%b %d, %Y')


@register_image_fields('photo')
class XArtModelItem(Item):
    name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    photo = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    brief = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    vote_score = Field(
        input_processor=MapCompose(str.strip, extract_vote_score, float),
        output_processor=TakeFirst()
    )
    vote_count = Field(
        input_processor=MapCompose(str.strip, extract_vote_count, int),
        output_processor=TakeFirst()
    )
    age = Field(
        input_processor=MapCompose(str.strip, intfy),
        output_processor=TakeFirst()
    )
    country = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )


@register_image_fields('cover', 'screenshots')
class XArtVideoItem(Item):
    name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    cover = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    screenshots = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Identity()
    )
    publish_time = Field(
        input_processor=MapCompose(str.strip, convert_datetime),
        output_processor=TakeFirst()
    )
    brief = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join()
    )
    cast = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Identity()
    )
    vote_score = Field(
        input_processor=MapCompose(str.strip, extract_vote_score, float),
        output_processor=TakeFirst()
    )
    vote_count = Field(
        input_processor=MapCompose(str.strip, extract_vote_count, int),
        output_processor=TakeFirst()
    )


@register_image_fields('images')
class XArtBlogPostItem(Item):
    title = Field()
    video = Field()
    images = Field()
    publish_time = Field()
    content = Field()
    love_count = Field()