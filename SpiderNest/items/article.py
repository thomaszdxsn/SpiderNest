"""
author: thomaszdxsn
"""
from scrapy import Item, Field

__all__ = ("InfoQCnArticleItem",)



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