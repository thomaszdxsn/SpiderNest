# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Response, Request
from scrapy.loader import ItemLoader

from ...items.ip import IPItem

__all__ = ('Ip66ipSpider',)


class Ip66ipSpider(scrapy.Spider):
    name = 'ip-ip66'
    allowed_domains = ['66ip.cn']
    start_urls = ['http://www.66ip.cn/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'DOWNLOAD_DELAY': 1
    }
    MAX_PAGE: int = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAX_PAGE = int(kwargs.get('max_page', 30))
        self.page = 1

    def parse(self, response: Response):
        for index, row in enumerate(response.css("table tr")):
            if index < 2:
                # 前两行不是有效数据
                continue
            loader = ItemLoader(item=IPItem(), selector=row)
            loader.add_value('source', 'ip66')
            loader.add_value('protocol', 'http')
            loader.add_css('ip', 'td:nth-child(1)::text')
            loader.add_css('port', 'td:nth-child(2)::text')
            loader.add_css('remark', 'td:nth-child(3)::text')
            yield loader.load_item()

        if self.page < self.MAX_PAGE:
            self.page += 1
            next_page = response.css('#PageList a:last-child::attr("href")').extract_first()
            yield Request(
                url=response.urljoin(next_page)
            )