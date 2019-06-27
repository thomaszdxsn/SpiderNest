"""
author: thomaszdxsn
"""
from ....spiders.sanguo.sanguo_ol import SanguoOlSpider, SanguoOlHeroItem


def test_spider_parse(resource_get):
    spider = SanguoOlSpider()

    start_req = next(spider.start_requests())
    resp = resource_get(start_req.url, request=start_req)

    parse_result = next(spider.parse(resp))
    assert isinstance(parse_result, SanguoOlHeroItem)