"""
author: thomaszdxsn
"""
from scrapy.http import Request

from ....spiders.leiyang.leiyang_estate import LyEstatePostSpider, LyEstatePostItem
from ....models.leiyang.estate import LyEstatePost


def test_ly_estate_post_spider_parse_method(resource_get):
    spider = LyEstatePostSpider()
    url = spider.start_urls[0]
    selector = resource_get(url)
    parsed_result = list(spider.parse(selector))
    assert len(parsed_result) > 0

    for result in parsed_result:
        assert isinstance(result, Request)
        assert result.callback in (spider.parse, spider.parse_detail)


def test_ly_estate_post_spider_parse_detail_method(resource_get):
    spider = LyEstatePostSpider()
    url = spider.start_urls[0]
    selector = resource_get(url)
    parsed_result = list(spider.parse(selector))
    detail_url = parsed_result[0].url

    detail_selector= resource_get(detail_url)
    parsed_result = list(spider.parse_detail(detail_selector))
    assert len(parsed_result) > 0
    for result in parsed_result:
        assert isinstance(result, LyEstatePostItem)
        assert LyEstatePost(**dict(result))