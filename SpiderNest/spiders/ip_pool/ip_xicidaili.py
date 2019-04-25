# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader

from ...items.ip import IPItem

__all__ = ("XicidailiSpider",)


class XicidailiSpider(scrapy.Spider):
    name = 'ip-xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'DOWNLOAD_DELAY': 1
    }
    MAX_PAGE: int = 10

    def __init__(self, *args, **kwargs):
        super(XicidailiSpider, self).__init__(*args, **kwargs)
        self.MAX_PAGE = int(kwargs.get('max_page', 10))
        self.page = 1

    def parse(self, response: Response):
        for index, row in enumerate(response.css('table#ip_list tr')):
            if index == 0:
                # 第一行是表头，不进行解析
                continue
            loader = ItemLoader(item=IPItem(), selector=row)
            loader.add_value('source', 'xicidaili')
            loader.add_css('ip', 'td:nth-child(2)::text')
            loader.add_css('port', 'td:nth-child(3)::text')
            loader.add_css('remark', 'td:nth-child(4) a::text')
            loader.add_css('protocol', 'td:nth-child(6)::text')

            item = loader.load_item()
            if not item.get('ip'):
                # 有时候有些row数据无效
                continue
            yield item

        if self.page < self.MAX_PAGE:
            self.page += 1
            next_page = 'https://www.xicidaili.com/nt/{}'.format(self.page)
            yield Request(
                url=response.urljoin(next_page),
                callback=self.parse
            )