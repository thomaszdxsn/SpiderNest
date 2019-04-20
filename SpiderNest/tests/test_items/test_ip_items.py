"""
author: thomaszdxsn
"""
import pytest
from scrapy.loader import ItemLoader

from SpiderNest.items.ip import IPItem
from SpiderNest.models.ip import IP


@pytest.mark.parametrize(
    'params',
    [
        ('0.1.125.221', '80', 'https', 'source', ['remark1', 'remark2'])
    ]
)
def test_ly_community_post_comment_item_with_processors(params):
    fields = [
        'ip', 'port', 'protocol', 'source', 'remark'
    ]
    loader = ItemLoader(item=IPItem(), base_url='http://lysq.com')
    for name, val in zip(fields, params):
        loader.add_value(name, val)
    item = loader.load_item()
    assert IP(**item)
