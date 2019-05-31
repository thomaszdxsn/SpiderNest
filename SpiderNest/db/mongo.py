"""
author: thomaszdxsn
"""
from typing import Type, Optional, Union

from scrapy.item import Item
from twisted.internet import defer
from dynaconf import settings as dync_settings
from txmongo.connection import ConnectionPool

from ..items.image import ImageItem

__all__ = ('insert_item',)


@defer.inlineCallbacks
def insert_item(spider_name: str, item: Type[Union[Item, dict]], connection_pool: Optional[ConnectionPool]=None):
    if not connection_pool:
        mongo = yield ConnectionPool(dync_settings['MONGO_URI'])
    else:
        mongo = connection_pool

    db = mongo[dync_settings.MONGO_DB_NAME]
    collection = db[spider_name]

    if isinstance(item, ImageItem):
        collection = db[dync_settings.IMAGE_COLLECTION]

    yield collection.insert(
        dict(item),
    )
