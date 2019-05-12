# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.internet import defer
from dynaconf import settings as dync_settings
from txmongo.connection import ConnectionPool


class MongoPipeline(object):

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        mongo = yield ConnectionPool(dync_settings['MONGO_URI'])

        db = mongo.spiderNest
        collection = db[spider.name]

        yield collection.insert(
            dict(item),
        )
        return item