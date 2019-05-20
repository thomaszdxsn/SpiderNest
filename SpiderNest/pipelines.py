# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.internet import defer

from SpiderNest.db.mongo import insert_item
from txmongo.connection import ConnectionPool
from dynaconf import settings as dync_settings


class MongoPipeline(object):

    @defer.inlineCallbacks
    def open_spider(self, spider):
        self.connection_pool = yield ConnectionPool(dync_settings['MONGO_URI'], pool_size=10)

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        yield insert_item(spider.name, item, connection_pool=self.connection_pool)
        # TODO: 加入超时时间，防止卡死
        return item