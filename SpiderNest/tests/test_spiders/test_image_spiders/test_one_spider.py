"""
author: thomaszdxsn
"""
from scrapy.http import Request

from ....spiders.images.one import OneSpider, OneImgItem


def test_OneSpider_start_requests():
    spider = OneSpider()

    req = next(spider.start_requests())
    assert isinstance(req, Request)


def test_OneSpider_parse_index(resource_get):
    spider = OneSpider()

    req = next(spider.start_requests())
    assert isinstance(req, Request)

    start_response = resource_get(req.url, request=req)
    parse_index_result = next(spider.parse_index(start_response))
    assert isinstance(parse_index_result, Request)


def test_OneSpider_parse_img(resource_get):
    spider = OneSpider()
    req = next(spider.start_requests())
    assert isinstance(req, Request)
    start_response = resource_get(req.url, request=req)
    parse_index_result = next(spider.parse_index(start_response))
    assert isinstance(parse_index_result, Request)

    img_response = resource_get(parse_index_result.url, request=parse_index_result)
    parse_img_result = next(spider.parse_img(img_response))
    assert isinstance(parse_img_result, OneImgItem)
