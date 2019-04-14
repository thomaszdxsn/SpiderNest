# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader

from ...items.ip import IPItem

__all__ = ('IpKuaidailiSpider',)


class IpKuaidailiSpider(scrapy.Spider):
    name = 'ip-kuaidaili'
    allowed_domains = ['kuaidaili.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }
    MAX_PAGE: int = 10

    def __init__(self, *args, **kwargs):
        super(IpKuaidailiSpider, self).__init__(*args, **kwargs)
        self.MAX_PAGE = int(kwargs.get('max_page', 10))

    def start_requests(self):
        start_urls = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]

        for url in start_urls:
            yield Request(url, callback=self.parse, meta={'page': 1, 'index_url': url})

    def parse(self, response: Response):
        for row in response.css('div#list table tbody tr'):
            loader = ItemLoader(item=IPItem(), selector=row)
            loader.add_value('source', 'kuaidaili')
            loader.add_css('ip', 'td[data-title="IP"]::text')
            loader.add_css('port', 'td[data-title="PORT"]::text')
            loader.add_css('protocol', 'td[data-title="类型"]::text')
            loader.add_css('remark', 'td[data-title="位置"]::text')
            yield loader.load_item()

        page = response.meta['page']
        if page < self.MAX_PAGE:
            next_page_num = page + 1
            next_page = "{}{}/".format(response.meta['index_url'], next_page_num)
            yield Request(
                url=next_page,
                callback=self.parse,
                meta={**response.meta, 'page': next_page_num}
            )