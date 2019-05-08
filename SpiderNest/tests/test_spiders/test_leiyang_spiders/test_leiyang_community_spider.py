"""
author: thomaszdxsn
"""
import pytest
from scrapy.item import Item
from scrapy.http import Request

from SpiderNest.spiders.leiyang.leiyang_community import LeiYangCommunitySpider
from SpiderNest.items.leiyang.community import LyCommunityUserItem, LyCommunityCommentItem
from SpiderNest.models.leiyang.community import LyCommunityPost, LyCommunityComment, LyCommunityUser

spider = LeiYangCommunitySpider()


@pytest.mark.parametrize('forum_block,url', [
    ('耒阳社区', 'http://www.lysq.com/forum-5-1.html'),
    ('社区水库', 'http://www.lysq.com/forum-6-1.html'),
    ('精彩活动', 'http://www.lysq.com/forum-114-1.html'),
    ('社区公益', 'http://www.lysq.com/forum-50-1.html'),
    ('微视自拍', 'http://www.lysq.com/forum-122-1.html'),
    ('旅游户外', 'http://www.lysq.com/forum-49-1.html'),
    ('原创文学', 'http://www.lysq.com/forum-35-1.html'),
    ('耒阳史记', 'http://www.lysq.com/forum-31-1.html'),
])
def test_spider_parse_forum_block_list(resource_get, request_factory, forum_block, url):
    req = request_factory(url, meta={
        'forum_block': forum_block,
        'page': 1
    })
    selector = resource_get(url, request=req)

    parse_result = spider.parse_forum_block_list(selector)
    yielded_results = list(parse_result)
    yielded_items = [item for item in yielded_results if isinstance(item, Item)]
    assert [LyCommunityPost(**dict(item)) for item in yielded_items]


@pytest.mark.parametrize('url', [
    'http://www.lysq.com/thread-47246-1-1.html'
])
def test_spider_parse_forum_post(resource_get, request_factory, url):
    req = request_factory(url, meta={
        'page': 1,
        'post_url': 'post_url'
    })
    selector = resource_get(url, request=req)
    parse_result = spider.parse_forum_post(selector)

    for item in parse_result:
        if isinstance(item, LyCommunityCommentItem):
            assert LyCommunityComment(**dict(item))
        elif isinstance(item, LyCommunityUserItem):
            assert LyCommunityUser(**dict(item))


def test_spider_start_request_will_ouput_request_for_forum_list_page():
    result = spider.start_requests()
    for item in result:
        assert isinstance(item, Request)
        assert item.callback == spider.parse_forum_block_list
        assert item.meta['page'] == 1
        assert item.meta['forum_block']

