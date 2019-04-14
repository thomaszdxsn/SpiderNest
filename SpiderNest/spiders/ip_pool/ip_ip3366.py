# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader

from ...items.ip import IPItem

__all__ = ("IpIp3366Spider",)


class IpIp3366Spider(scrapy.Spider):
    name = 'ip-ip3366'
    allowed_domains = ['ip3366.net']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'DOWNLOAD_DELAY': 1
    }

    MAX_PAGE: int = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAX_PAGE = int(kwargs.get('max_page', 10))
        self.page = 1

    def start_requests(self):
        start_urls = [
            'http://www.ip3366.net/free/?stype=1',
            'http://www.ip3366.net/free/?stype=2'
        ]
        for url in start_urls:
            yield Request(url, callback=self.parse, meta={'index_url': url})

    def parse(self, response: Response):
        for row in response.css('table tbody tr'):
            loader = ItemLoader(item=IPItem(), selector=row)
            loader.add_value('source', 'ip3366')
            loader.add_css('ip', 'td:nth-child(1)::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            loader.add_css('protocol', 'td:nth-child(4)::text')
            loader.add_css('remark', 'td:nth-child(5)::text')
            yield loader.load_item()

        if self.page < self.MAX_PAGE:
            self.page += 1
            next_page = f'{response.meta["index_url"]}&page={self.page}'
            yield Request(next_page, callback=self.parse, meta=response.meta)
