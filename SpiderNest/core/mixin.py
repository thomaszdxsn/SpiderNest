"""
author: thomaszdxsn
"""
from typing import Type

__all__ = ('item_default_val_mixin_factory',)


class ItemMixin:
    pass


def item_default_val_mixin_factory(**default_values) -> Type[ItemMixin]:
    assert default_values, '不可以传入空的默认值'

    class _ItemMixin(ItemMixin):

        def __init__(self, *args, **kwargs):
            for k, v in default_values.items():
                kwargs.setdefault(k, v if not callable(v) else v())
            super().__init__(*args, **kwargs)

    return _ItemMixin