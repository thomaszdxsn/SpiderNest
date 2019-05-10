import json
import itertools
from typing import Dict, Any, Union, List
from types import ModuleType

from scrapy.http import TextResponse as scrapyResponse
from requests import Response as requestsResponse

__all__ = ('load_json_response', 'union_modules_enter_points')

JSONType = Union[
    Dict[str, Any],
    List[Any],
]


def load_json_response(response: Union[scrapyResponse, requestsResponse]) -> JSONType:
    if isinstance(response, scrapyResponse):
        return json.loads(response.body.decode())
    else:
        return response.json()


def union_modules_enter_points(*modules: ModuleType):
    return tuple(itertools.chain.from_iterable(mod.__all__ for mod in modules))
