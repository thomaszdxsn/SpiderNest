"""
author: thomaszdxsn
"""
from typing import Type, TYPE_CHECKING

from scrapy.loader import ItemLoader
from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    T_Pydantic_Model = Type[BaseModel]

__all__ = ('SchemaItemLoader',)


class SchemaItemLoader(ItemLoader):

    def __init__(self, **kwargs):
        self.model: 'T_Pydantic_Model' = kwargs.pop('model', None)
        assert self.model, '必须提供一个model，用来供validate使用'
        super(SchemaItemLoader, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        try:
            item = self.load_item()
            self.model(**item)
        except ValidationError:
            return False
        return True