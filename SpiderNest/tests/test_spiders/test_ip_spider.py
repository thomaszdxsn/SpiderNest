"""
author: thomaszdxsn
"""
from scrapy.http import Request

from ...spiders.ip_pool import (IpKuaidailiSpider, Ip66ipSpider, IpCoolproxySpider, IpProxylistSpider, IpData5uSpider,
                                XicidailiSpider, IpIp3366Spider, ProxydbSpider)
from ...items.ip import IPItem
from ...models.ip import IP


def test_ip_kuaidaili_spider(resource_get):
    spider = IpKuaidailiSpider()

    for req in spider.start_requests():
        selector = resource_get(req.url, request=req)

        result = spider.parse(selector)

        for item in result:
            if isinstance(item, IPItem):
                assert IP(**dict(item))
            elif isinstance(item, Request):
                # next page
                assert item.url.startswith(req.url)
            else:
                raise ValueError('yield 输出了意料外的item')


def test_ip_66_spider(resource_get):
    spider = Ip66ipSpider()

    url = spider.start_urls[0]
    selector = resource_get(url)
    result = spider.parse(selector)

    for item in result:
        if isinstance(item, IPItem):
            assert IP(**dict(item))
        elif isinstance(item, Request):
            assert item.url.startswith(url)
        else:
            raise ValueError('yield 输出了意料外的item')


def test_coolproxy_spider(resource_get):
    spider = IpCoolproxySpider()

    url = spider.start_urls[0]
    headers = {
        'user-agent': spider.custom_settings['USER_AGENT']
    }
    selector = resource_get(url, headers=headers)

    result = spider.parse(selector)
    for item in result:
        if isinstance(item, IPItem):
            assert IP(**dict(item))
        elif isinstance(item, Request):
            assert item.url.startswith(url)
        else:
            raise ValueError('yield 输出了意料外的item')


def test_proxy_list_spider(resource_get):
    spider = IpProxylistSpider()

    url = spider.start_urls[0]
    headers = {
        'user-agent': spider.custom_settings['USER_AGENT']
    }
    selector = resource_get(url, headers=headers)

    result = spider.parse(selector)
    for item in result:
        if isinstance(item, IPItem):
            assert IP(**dict(item))
        elif isinstance(item, Request):
            assert item.url.startswith(url)
        else:
            raise ValueError('yield 输出了意料外的item')


def test_proxy_data5u_spider(resource_get):
    spider = IpData5uSpider()
    headers = {
        'user-agent': spider.custom_settings['USER_AGENT']
    }

    for req in spider.start_requests():
        selector = resource_get(req.url, headers=headers, request=req)

        result = spider.parse(selector)
        for item in result:
            if isinstance(item, IPItem):
                assert IP(**dict(item))
            elif isinstance(item, Request):
                assert item.url.startswith(req.url)
            else:
                raise ValueError('yield 输出了意料外的item')
                
                
def test_proxydb_spider(resource_get):
    spider = ProxydbSpider()

    url = spider.start_urls[0]
    headers = {
        'user-agent': spider.custom_settings['USER_AGENT']
    }
    selector = resource_get(url, headers=headers)
    
    result = spider.parse(selector)
    for item in result:
        if isinstance(item, IPItem):
            assert IP(**dict(item))
        else:
            raise ValueError('yield 输出了意料外的item')


def test_xicidaili_spider(resource_get):
    spider = XicidailiSpider()

    url = spider.start_urls[0]
    headers = {
        'user-agent': spider.custom_settings['USER_AGENT']
    }
    selector = resource_get(url, headers=headers)

    result = spider.parse(selector)
    for item in result:
        if isinstance(item, IPItem):
            assert IP(**dict(item))
        elif isinstance(item, Request):
            assert item.url.startswith(url)
        else:
            raise ValueError('yield 输出了意料外的item')


def test_ip3366_spider(resource_get):
    spider = IpIp3366Spider()
    headers = {
        'user-agent': spider.custom_settings['USER_AGENT']
    }

    for req in spider.start_requests():
        selector = resource_get(req.url, headers=headers, request=req)

        result = spider.parse(selector)
        for item in result:
            if isinstance(item, IPItem):
                assert IP(**dict(item))
            elif isinstance(item, Request):
                assert item.url.startswith(req.url)
            else:
                raise ValueError('yield 输出了意料外的item')
