"""
author: thomaszdxsn
"""
import warnings
from typing import Callable

import pathlib
import pytest
from scrapy.http import HtmlResponse, Request

import betamax
from betamax.fixtures.pytest import _betamax_recorder

warnings.simplefilter('ignore', category=DeprecationWarning)


# betamax配置
cassette_dir = pathlib.Path(__file__).parent / 'fixture' / 'cassettes'
cassette_dir.mkdir(parents=True, exist_ok=True)
with betamax.Betamax.configure() as config:
    config.cassette_library_dir = cassette_dir.resolve()
    config.preserve_exact_body_bytes = True


@pytest.fixture
def betamax_recorder(request):
    return _betamax_recorder(request, parametrized=True)


@pytest.fixture
def resource_get(betamax_session):

    def get(url, *args, **kwargs):
        request = kwargs.pop('request', None)
        resp = betamax_session.get(url, *args, **kwargs)
        selector = HtmlResponse(body=resp.content, url=url, request=request)
        return selector

    return get


@pytest.fixture
def request_factory():

    def _request_factory(url, *args, **kwargs):
        return Request(url, *args, **kwargs)

    return _request_factory