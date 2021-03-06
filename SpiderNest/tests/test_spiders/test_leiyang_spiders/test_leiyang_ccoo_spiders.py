"""
author: thomaszdxsn
"""
from scrapy.http import Request

from SpiderNest.spiders.leiyang.leiyang_ccoo import LeiyangCcooRecruitSpider
from SpiderNest.items.leiyang.ccoo import LyCcooRecruitmentItem
from SpiderNest.models.leiyang.ccoo import LyCcooRecruitmentInfo


def test_ly_ccoo_recruitment_spider_parse_method(resource_get):
    spider = LeiyangCcooRecruitSpider()
    url = spider.start_urls[0]
    selector = resource_get(url)
    parse_result = list(spider.parse(selector))
    assert len(parse_result) > 0

    for yield_result in parse_result:
        assert isinstance(yield_result, Request)
        assert yield_result.callback in (spider.parse_detail, spider.parse)


def test_ly_ccoo_recruitment_spider_parse_detail_method(resource_get):
    spider = LeiyangCcooRecruitSpider()
    list_url = spider.start_urls[0]
    selector = resource_get(list_url)
    parse_result = spider.parse(selector)
    detail_url = next(parse_result).url

    selector = resource_get(detail_url)
    parse_result = list(spider.parse_detail(selector))
    assert len(parse_result) > 0

    for yield_result in parse_result:
        assert isinstance(yield_result, LyCcooRecruitmentItem)
        assert LyCcooRecruitmentInfo(**yield_result)