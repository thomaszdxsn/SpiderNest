# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader

from ...items.ip import IPItem


class IpData5uSpider(scrapy.Spider):
    name = 'ip-data5u'
    allowed_domains = ['data5u.com']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        start_urls = [
            'http://www.data5u.com/free/index.shtml',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gwpt/index.shtml'
        ]
        for url in start_urls:
            yield Request(
                url,
                callback=self.parse
            )

    def parse(self, response: Response):
        for row in response.css('div.wlist ul.l2'):
            loader = ItemLoader(item=IPItem(), selector=row)
            loader.add_value('source', 'data5u')
            loader.add_css('ip', 'span:nth-child(1) li::text')
            loader.add_css('port', 'span:nth-child(2) li::text')
            loader.add_css('protocol', 'span:nth-child(4) li::text')
            loader.add_css('remark', 'span:nth-child(5) li::text')
            loader.add_css('remark', 'span:nth-child(5) li::text')
            yield loader.load_item()
