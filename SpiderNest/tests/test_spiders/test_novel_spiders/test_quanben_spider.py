import pytest
from scrapy.http import Request

from SpiderNest.spiders.novel.quanben import QuanbenXiaoshuoSpider, QuanbenBookItem


@pytest.mark.parametrize('raw,result', [
    ['第1章 地狱灵芝', ('地狱灵芝',)],
    ['第1752章 丹圣对决', ('丹圣对决',)]
])
def test_match_CHAPTER_NAME_PATTNER(raw, result):
    p = QuanbenXiaoshuoSpider._CHAPTER_NAME_PATTERN
    assert p.match(raw).groups() == result


@pytest.mark.parametrize('raw,dict_result', [
    [
        "setTimeout(\"ajax_post('book','ajax','pinyin','aoshidanshen','id','1','sky','ac1920c94d12c8d7e2159e29d3935c23','t','1561823180')\",\"1000\");",
        {'c': 'book', 'a': 'ajax', 'pinyin': 'aoshidanshen', 'id': '1', 'sky': 'ac1920c94d12c8d7e2159e29d3935c23', 't': '1561823180'}
    ]
])
def test_match_AJAX_PARAMS_PATTERN(raw, dict_result):
    p = QuanbenXiaoshuoSpider._AJAX_PARAMS_PATTERN
    assert p.match(raw).groupdict() == dict_result


def test_spider_parse_book_list(resource_get):
    spider = QuanbenXiaoshuoSpider()
    start_request = next(spider.start_requests())
    resp = resource_get(start_request.url, request=start_request)
    parse_book_list_result = spider.parse_book_list(resp)

    for yield_item in parse_book_list_result:
        assert isinstance(yield_item, (QuanbenBookItem, Request))
