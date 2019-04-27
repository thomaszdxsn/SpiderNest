"""
author: thomaszdxsn
"""
from collections import Counter

import pytest
from scrapy.http import Request

from ....spiders.leiyang.leiyang_estate import (
    LyEstatePostSpider, LyEstatePostItem, LyEstateInfoSpider, EstateType, LyEstateNewItem,
    LyEstateSecondItem, LyEstateRentItem
)
from ....models.leiyang.estate import LyEstatePost, LyEstateNewInfo, LyEstateSecondHandInfo, LyEstateRentInfo


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


def test_ly_estate_info_spider_start_requests_method():
    spider = LyEstateInfoSpider()
    counter = Counter()
    for yield_result in spider.start_requests():
        counter.update({
            yield_result.meta['type']: 1
        })

    for type_ in EstateType:
        assert counter[type_] == 1


def test_ly_estate_info_spider_parse_new_method(resource_get, request_factory):
    spider = LyEstateInfoSpider()
    url = spider.urls[EstateType.NEW]
    req = request_factory(url, meta={'type': EstateType.NEW})
    list_selector = resource_get(url, request=req)
    list_results = spider.parse(list_selector)
    detail_request = next(list_results)

    detail_selector = resource_get(detail_request.url, request=detail_request)
    detail_results = spider.parse_new(detail_selector)
    detail_new_request = next(detail_results)

    detail_desc_selector = resource_get(detail_new_request.url, request=detail_new_request)
    detail_desc_results = spider.parse_new_description(detail_desc_selector)
    detail_new_item = next(detail_desc_results)
    assert isinstance(detail_new_item, LyEstateNewItem)
    assert LyEstateNewInfo(**dict(detail_new_item))

    with pytest.raises(StopIteration):
        next(detail_desc_results)


def test_ly_estate_info_spider_parse_secondhandle_method(resource_get, request_factory):
    spider = LyEstateInfoSpider()
    url = spider.urls[EstateType.SECOND_HAND]
    req = request_factory(url, meta={'type': EstateType.SECOND_HAND})
    list_selector = resource_get(url, request=req)
    list_results = spider.parse(list_selector)
    detail_request = next(list_results)

    detail_selector = resource_get(detail_request.url, request=detail_request)
    detail_results = list(spider.parse_second_hand(detail_selector))
    assert len(detail_results) > 0

    for result in detail_results:
        assert isinstance(result, LyEstateSecondItem)
        assert LyEstateSecondHandInfo(**dict(result))


def test_ly_estate_info_spider_parse_rent_method(resource_get, request_factory):
    spider = LyEstateInfoSpider()
    url = spider.urls[EstateType.RENT]
    req = request_factory(url, meta={'type': EstateType.RENT})
    list_selector = resource_get(url, request=req)
    list_results = spider.parse(list_selector)
    detail_request = next(list_results)

    detail_selector = resource_get(detail_request.url, request=detail_request)
    detail_results = list(spider.parse_rent(detail_selector))
    assert len(detail_results) > 0

    for result in detail_results:
        assert isinstance(result, LyEstateRentItem)
        assert LyEstateRentInfo(**dict(result))