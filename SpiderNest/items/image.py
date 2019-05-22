"""
author: thomaszdxsn
"""
from typing import List

from scrapy.item import Item, Field

__all__ = ("ImageItem",)


def extract_image_items(spider_name: str, item: Item) -> List["ImageItem"]:
    fields = getattr(item, "_img_fields", [])
    return [
        ImageItem(
            spider_name=spider_name,
            key=f,
            image_urls=item[f] if isinstance(item[f], list) else [item[f]],
        )
        for f in fields
    ]


class ImageItem(Item):
    spider_name = Field()
    key = Field()
    image_urls = Field()
    images = Field()