"""
author: thomaszdxsn
"""
import pytest

from ...spiders.leiyang.leiyang_community import LeiYangCommunitySpider


@pytest.mark.parametrize('forum_block,url', [
    ('耒阳社区', 'http://www.lysq.com/forum-5-1.html'),
    ('社区水库', 'http://www.lysq.com/forum-6-1.html'),
])
def test_spider_parse_forum_block_list(resource_get, request_factory, forum_block, url):
    spider = LeiYangCommunitySpider()
    req = request_factory(url, meta={
        'forum_block': forum_block,
        'page': 1
    })
    selector = resource_get(url, request=req)

    parse_result = spider.parse_forum_block_list(selector)
    print(parse_result, next(parse_result))
