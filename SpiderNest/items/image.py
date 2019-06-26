"""
author: thomaszdxsn
"""
from typing import Generator, Type, Callable

from scrapy.item import Item, Field

__all__ = ("ImageItem", 'register_image_fields')

IMAGE_ATTR = '_img_fields'
T_ITEM = Type[Item]
T_WRAPPER = Callable[[T_ITEM], T_ITEM]


def extract_image_items(spider_name: str, item: Item) -> Generator["ImageItem", None, None]:
    fields = getattr(item, IMAGE_ATTR, [])
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


def register_image_fields(*fields: str) -> T_WRAPPER:

    def wrapper(cls):
        setattr(cls, IMAGE_ATTR, fields)
        return cls

    return wrapper
