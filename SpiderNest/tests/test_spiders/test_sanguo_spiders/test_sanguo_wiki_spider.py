"""
author: thomaszdxsn
"""
from scrapy.http import Request

from SpiderNest.spiders.sanguo.sanguo_wiki import SanguoWikiSpider, SanguoWikiCharacterItem


def test_parse_method_will_emit_request(resource_get):
    spider = SanguoWikiSpider()
    selector = resource_get(spider.start_urls[0])
    parse_result = spider.parse(selector)
    yield_result = next(parse_result)

    assert isinstance(yield_result, Request)


def test_parse_detail_method_will_emit_item(resource_get):
    spider = SanguoWikiSpider()
    selector = resource_get(spider.start_urls[0])
    parse_result = spider.parse(selector)
    yield_result = next(parse_result)

    detail_selector = resource_get(yield_result.url, request=yield_result)
    parse_detail_result = spider.parse_detail(detail_selector)
    yield_result = next(parse_detail_result)

    assert isinstance(yield_result, SanguoWikiCharacterItem)