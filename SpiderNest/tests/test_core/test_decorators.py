from scrapy import Item, Field

from ...core.decorators import item_default_val


def test_item_default_val():

    @item_default_val(field1='test')
    class CustomItem(Item):
        field1 = Field()
        field2 = Field()

    item = CustomItem()
    assert item['field1'] == 'test'
    assert item.get('field2', None) is None