"""
author: thomaszdxsn
"""
import arrow
import pytest
from scrapy.loader import ItemLoader

from SpiderNest.items.leiyang import LyCommunityPostItem
from SpiderNest.items.leiyang.processors import created_time_input_processor, strip_datetime_fields
from SpiderNest.models.leiyang import LyCommunityPost


@pytest.mark.parametrize(
    'raw_time,result',
    [
        ('2017-5-30', arrow.get('2017-5-30').replace(tzinfo='Asia/Shanghai')),
        ('13 小时前', arrow.now().shift(hours=-13)),
        ('4 天前', arrow.now().shift(days=-4)),
        ('昨天 10:31', arrow.get('{} 10:31'.format(format(arrow.now().shift(days=-1).datetime, '%Y-%m-%d')))),
        ('前天 09:40', arrow.get('{} 09:40'.format(format(arrow.now().shift(days=-2).datetime, '%Y-%m-%d'))))
    ]
)
def test_created_time_input_processor(raw_time, result):
    assert created_time_input_processor(raw_time) == strip_datetime_fields(result, ['second', 'microsecond'])


@pytest.mark.parametrize(
    'params',
    [
        ('block', 'title', 'url', 'username', 0, 0, True, True, '2018-01-01', '2018-01-01', 'username'),
            ('block', 'title', 'url', 'username', 0, 0, True, True, '半小时前', '40 分钟前', 'username'),
    ]
)
def test_ly_community_post_item_with_input_processors(params):
    fields = ['block_name', 'title', 'url', 'author_username', 'view_count', 'comment_count', 'has_attachment',
              'has_image', 'created_time', 'last_comment_time', 'last_comment_username']
    loader = ItemLoader(item=LyCommunityPostItem())
    for name, val in zip(fields, params):
        loader.add_value(name, val)
    item = loader.load_item()
    assert LyCommunityPost(**item)