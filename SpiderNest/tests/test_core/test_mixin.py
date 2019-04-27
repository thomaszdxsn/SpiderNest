"""
author: thomaszdxsn
"""
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader

from ...core.mixin import item_default_val_mixin_factory


def test_item_default_val_mixin():
    Mixin = item_default_val_mixin_factory(a='b')

    class ExampleItem(Mixin, Item):
        a = Field()

    item = ExampleItem()
    assert item['a'] == 'b'

    item = ExampleItem(a='c')
    assert item['a'] == 'c'

    loader = ItemLoader(item=ExampleItem())
    item = loader.load_item()
    assert item['a'] == 'b'

    loader.add_value('a', 'c')
    item = loader.load_item()
    assert item['a'] == ['c']