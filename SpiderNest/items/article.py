"""
author: thomaszdxsn
"""
from scrapy import Item, Field

from .image import register_image_fields

__all__ = ("InfoQCnArticleItem",)


@register_image_fields('cover')
class ArticleItem(Item):
    url = Field()
    cover = Field()
    title = Field()
    summary = Field()
    author_name = Field()
    content = Field()
    publish_time = Field()


class InfoQCnArticleItem(ArticleItem):
    uuid = Field()
    topics = Field()
    view_count = Field()
    subtitle = Field()
    author_names = Field()