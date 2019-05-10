"""
author: thomaszdxsn
"""
import warnings
from typing import Callable

import pathlib
import pytest
from scrapy.http import TextResponse, Request

import betamax
from betamax.fixtures.pytest import _betamax_recorder

warnings.simplefilter('ignore', category=DeprecationWarning)


# betamax配置
cassette_dir = pathlib.Path(__file__).parent / 'fixture' / 'cassettes'
cassette_dir.mkdir(parents=True, exist_ok=True)
with betamax.Betamax.configure() as config:
    config.cassette_library_dir = cassette_dir.resolve()
    config.preserve_exact_body_bytes = True
    config.default_cassette_options['record_mode'] = 'once'


@pytest.fixture
def betamax_recorder(request):
    record = _betamax_recorder(request, parametrized=True)
    return record


@pytest.fixture
def switch_betamax_new_episode():
    with betamax.Betamax.configure() as config:
        config.default_cassette_options['record_mode'] = 'new_episodes'
        yield
        config.default_cassette_options['record_mode'] = 'once'


@pytest.fixture
def resource_get(betamax_session):

    def get(url, *args, **kwargs):
        request = kwargs.pop('request', None)
        resp = betamax_session.get(url, *args, **kwargs)
        selector = TextResponse(body=resp.content, url=url, request=request, headers=resp.headers)
        return selector

    return get


@pytest.fixture
def resource_post(betamax_session):
    def get(url, *args, **kwargs):
        request = kwargs.pop('request', None)
        resp = betamax_session.post(url, *args, **kwargs)
        selector = TextResponse(body=resp.content, url=url, request=request, headers=resp.headers)
        return selector

    return get


@pytest.fixture
def request_factory():

    def _request_factory(url, *args, **kwargs):
        return Request(url, *args, **kwargs)

    return _request_factory