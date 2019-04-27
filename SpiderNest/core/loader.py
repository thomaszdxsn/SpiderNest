"""
author: thomaszdxsn
"""
import logging
from typing import Type, TYPE_CHECKING

from scrapy.loader import ItemLoader
from pydantic import BaseModel, ValidationError

if TYPE_CHECKING:
    T_Pydantic_Model = Type[BaseModel]

__all__ = ('SchemaItemLoader',)
logger = logging.getLogger(__name__)


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
            logger.exception('验证格式错误')
            return False
        return True