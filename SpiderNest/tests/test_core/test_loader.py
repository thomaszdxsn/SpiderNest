"""
author: thomaszdxsn
"""
import pytest

from ...core.loader import SchemaItemLoader
from ...items.ip import IPItem
from ...models.ip import IP


def test_init_without_model_will_raise_a_error():
    with pytest.raises(AssertionError):
        SchemaItemLoader()


def test_loader_validate_method():
    loader = SchemaItemLoader(item=IPItem(), model=IP)
    for field in ('ip', 'source', 'port', 'protocol', 'remark'):
        loader.add_value(field, field)

    assert loader.is_valid()
