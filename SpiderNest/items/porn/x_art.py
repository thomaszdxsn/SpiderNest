"""
author: thomaszdxsn
"""
from scrapy import Field, Item

from ..image import register_image_fields

__all__ = ("XArtModel", "XArtVideo", "XArtBlogPost")


@register_image_fields('photo')
class XArtModel(Item):
    name = Field()
    photo = Field()
    brief = Field()
    vote_score = Field()
    vote_count = Field()
    age = Field()
    country = Field()


@register_image_fields('cover', 'screenshots')
class XArtVideo(Item):
    name = Field()
    cover = Field()
    screenshots = Field()
    publish_time = Field()
    brief = Field()
    vote_score = Field()
    vote_count = Field()
    comment_list = Field()


@register_image_fields('images')
class XArtBlogPost(Item):
    title = Field()
    video = Field()
    images = Field()
    publish_time = Field()
    content = Field()
    love_count = Field()