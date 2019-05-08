"""
author: thomaszdxsn
"""
from scrapy import Request

from ....spiders.leiyang.leiyang_community import LeiyangCommnuity114Spider, Ly114Item
from ....models.leiyang.community import Ly114Info



def test_spider_parse_index(resource_get):
    spider = LeiyangCommnuity114Spider()
    request = next(spider.start_requests())

    selector = resource_get(request.url, request=request)
    parse_result = spider.parse_index(selector)
    yield_result = next(parse_result)

    assert isinstance(yield_result, Request)
    assert 'formhash' in yield_result.url
    assert yield_result.callback == spider.parse


def test_spider_parse(switch_betamax_new_episode, resource_get):
    spider = LeiyangCommnuity114Spider()
    request = next(spider.start_requests())

    selector = resource_get(request.url, request=request)
    parse_result = spider.parse_index(selector)
    yield_result = next(parse_result)

    list_selector = resource_get(yield_result.url, request=yield_result)
    parse_result = spider.parse(list_selector)
    list_result = list(parse_result)
    assert all(
        req.callback in (spider.parse, spider.parse_detail)
        for req in list_result
    )


def test_spider_parse_detail(switch_betamax_new_episode, resource_get):
    spider = LeiyangCommnuity114Spider()
    request = next(spider.start_requests())

    selector = resource_get(request.url, request=request)
    parse_result = spider.parse_index(selector)
    yield_result = next(parse_result)

    list_selector = resource_get(yield_result.url, request=yield_result)
    parse_result = spider.parse(list_selector)

    detail_request = next(parse_result)
    detail_selector = resource_get(detail_request.url, request=detail_request)
    parse_result = spider.parse_detail(detail_selector)

    item = next(parse_result)
    assert Ly114Info(**item)