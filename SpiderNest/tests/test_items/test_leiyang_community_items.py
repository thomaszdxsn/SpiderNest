"""
author: thomaszdxsn
"""
import arrow
import pytest
from scrapy.loader import ItemLoader

from SpiderNest.items.leiyang import LyCommunityPostItem, LyCommunityUserItem, LyCommunityCommentItem, Ly114Item
from SpiderNest.items.processors import created_time_input_processor, strip_datetime_fields
from SpiderNest.models.leiyang import LyCommunityPost, LyCommunityUser, LyCommunityComment, Ly114Info


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
def test_ly_community_post_item_with_processors(params):
    fields = ['block_name', 'title', 'url', 'author_username', 'view_count', 'comment_count', 'has_attachment',
              'has_image', 'created_time', 'last_comment_time', 'last_comment_username']
    loader = ItemLoader(item=LyCommunityPostItem(), base_url='http://lysq.com')
    for name, val in zip(fields, params):
        loader.add_value(name, val)
    item = loader.load_item()
    assert LyCommunityPost(**item)


@pytest.mark.parametrize(
    'params',
    [
        ('username', 'http://aaaa', '1', '2', '3', '4', [1], None, 'level1')
    ]
)
def test_ly_community_post_user_item_with_processors(params):
    fields = ['username', 'avatar_url', 'topic_count', 'post_count', 'credit_count', 'coin_count',
              'medal_list', 'signature', 'user_group']
    loader = ItemLoader(item=LyCommunityUserItem(), base_url='http://lysq.com')
    for name, val in zip(fields, params):
        loader.add_value(name, val)
    item = loader.load_item()
    assert LyCommunityUser(**item)


@pytest.mark.parametrize(
    'params',
    [
        ('url', 'username', 1, '2019-1-1', 'content', '', [1])
    ]
)
def test_ly_community_post_comment_item_with_processors(params):
    fields = [
        'post_url', 'author_username', 'floor', 'created_time', 'content', 'signature', 'image_urls'
    ]
    loader = ItemLoader(item=LyCommunityCommentItem(), base_url='http://lysq.com')
    for name, val in zip(fields, params):
        loader.add_value(name, val)
    item = loader.load_item()
    assert LyCommunityComment(**item)


@pytest.mark.parametrize(
    'params',
    [
        {
            'category': ['便民服务'],
            'cover': ['http://www.lysq.com/source/plugin/xigua_114/static/nologo.png'],
            'name': [' 耒阳市兴旺搬家公司'],
            'phone': ['13975475475123']
        },

        {
            'address': ['衡阳市耒阳市国贸新城新步步高5楼'],
            'category': ['中小学校'],
            'cover': ['http://www.lysq.com/source/plugin/xigua_114/upload/gg5911ac1ee6ebb6171.gif.gif'],
            'description': ['来Bingo，爸妈再也不用担心我的学习'],
            'name': ['Bingo教育培训学校'],
            'phone': ['0734-4928111'],
            'qq': ['2108079194'],
            'wechat': ['Bingowy']
        },
        {
            'address': ['衡阳市耒阳市神农路(蔡伦北路路口北)'],
            'category': ['家政服务'],
            'cover': ['http://www.lysq.com/source/plugin/xigua_114/static/nologo.png'],
            'description': [' 广州家事无忧耒阳分公司 纸都家政服务有限公司！ 我们拥有专业的团队， 专业设备， 还有专业家政师为您提供服务！  '
                         '服务项目： 新房开荒保洁 家电保洁，保养， 各种沙发的清洗，保养… 还承接各区域 宾馆 酒店 医院 饭店 大厦 文化广场 '
                         '写字楼 别墅 物业公司， 日常保洁和清洗养护！ 服务地址：耒阳市神农路   号栖凤园居委会对面服务电话 '
                         '07344726699     13397476599'],
            'name': ['耒阳市纸都家政服务'],
            'phone': ['07344726699'],
            'qq': ['462344894'],
            'wechat': ['13397476599                        ',
                    '\r\n                    ',
                    'http://www.lysq.com/source/plugin/xigua_114/upload/gg581700c1cc1657051.jpg.jpg']
        }
    ]
)
def test_ly_114_item_with(params):
    loader = ItemLoader(item=Ly114Item())
    for k, v in params.items():
        loader.add_value(k, v)

    item = loader.load_item()
    assert Ly114Info(**item)