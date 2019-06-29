"""
author: thomaszdxsn
"""
from scrapy.http import Request

from SpiderNest.items.porn import XArtModelItem, XArtVideoItem, XArtBlogPostItem
from ....spiders.porn.x_art import XArtSpider


def test_spider_parse_model_detail(resource_get):
    spider = XArtSpider()
    list_resp = resource_get(spider._model_list_url)
    parse_list_results = spider.parse_model_list(list_resp)

    detail_req = next(parse_list_results)
    assert isinstance(detail_req, Request)
    detail_resp = resource_get(detail_req.url, request=detail_req)
    parse_detail_result = next(spider.parse_model_detail(detail_resp))
    assert isinstance(parse_detail_result, XArtModelItem)


def test_spider_parse_video_detail(resource_get):
    spider = XArtSpider()
    list_resp = resource_get(spider._video_list_url)
    parse_list_results = spider.parse_video_list(list_resp)

    detail_req = next(parse_list_results)
    assert isinstance(detail_req, Request)
    detail_resp = resource_get(detail_req.url, request=detail_req)
    parse_detail_result = next(spider.parse_video_detail(detail_resp))
    assert isinstance(parse_detail_result, XArtVideoItem)


def test_spider_parse_blog_post_detail(resource_get):
    spider = XArtSpider()
    headers = {'User-Agent': spider.custom_settings['USER_AGENT']}
    list_resp = resource_get(spider._blog_list_url, headers=headers)
    parse_list_results = spider.parse_blog_list(list_resp)

    detail_req = next(parse_list_results)
    assert isinstance(detail_req, Request)
    detail_resp = resource_get(detail_req.url, request=detail_req, headers=headers)
    parse_detail_result = next(spider.parse_blog_detail(detail_resp))
    assert isinstance(parse_detail_result, XArtBlogPostItem)