"""
author: thomaszdxsn
"""
from typing import Generator

from scrapy.item import Item, Field

__all__ = ("ImageItem",)


def extract_image_items(spider_name: str, item: Item) -> Generator["ImageItem", None, None]:
    fields = getattr(item, "_img_fields", [])
    return (
        ImageItem(
            spider_name=spider_name,
            item_name=type(item).__name__,
            key=f,
            image_urls=item[f] if isinstance(item[f], list) else [item[f]],
        )
        for f in fields
    )


class ImageItem(Item):
    spider_name = Field()
    item_name = Field()
    key = Field()
    image_urls = Field()
    images = Field()