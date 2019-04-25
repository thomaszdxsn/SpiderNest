# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Response, Request
from scrapy.loader import ItemLoader

from ...items.ip import IPItem

__all__ = ('IpProxylistSpider',)


class IpProxylistSpider(scrapy.Spider):
    name = 'ip-proxylist'
    start_urls = ['http://proxylist.me/?sort=-updated']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'DOWNLOAD_DELAY': 5
    }
    MAX_PAGE: int=30
    
    def __init__(self, *args, **kwargs):
        super(IpProxylistSpider, self).__init__(*args, **kwargs)
        self.MAX_PAGE = int(kwargs.get('max_page', 30))
        self.page = 1

    def parse(self, response: Response):
        for row in response.css('#datatable-row-highlight tbody tr'):
            if len(row.css('td')) != 9:
                continue
            loader = ItemLoader(item=IPItem(), selector=row)
            loader.add_value('source', 'proxylist')
            loader.add_css('ip', 'td:nth-child(1) a::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            loader.add_css('protocol', 'td:nth-child(4)::text')
            loader.add_css('remark', 'td:nth-child(5)::text')

            yield loader.load_item()

        if self.page < self.MAX_PAGE:
            self.page += 1
            yield Request(
                url=self.start_urls[0] + f'&page={self.page}',
                callback=self.parse
            )
            
