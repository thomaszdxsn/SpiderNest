from scrapy import Item, Field
import pytest

from ...core.decorators import item_default_vals
from ...items.image import register_image_fields


def test_item_default_vals():

    @item_default_vals(field1='test')
    class CustomItem(Item):
        field1 = Field()
        field2 = Field()

    item = CustomItem()
    assert item['field1'] == 'test'
    assert item.get('field2', None) is None


def test_item_default_callable():

    @item_default_vals(field1=lambda: 'test')
    class CustomItem(Item):
        field1 = Field()
        field2 = Field()

    item = CustomItem()
    assert item['field1'] == 'test'
    assert item.get('field2', None) is None


def test_register_image_fields():

    @register_image_fields('field1')
    class CustomItem(Item):
        field1 = Field()
        field2 = Field()

    item = CustomItem()
    assert len(item._img_fields) == 1
    assert item._img_fields[0] == 'field1'


def test_register_image_fields_raise_exception_when_field_not_include_in_class_body():

    with pytest.raises(AssertionError):
        @register_image_fields('field3')
        class CustomItem(Item):
            field1 = Field()
            field2 = Field()

