# -*- coding: utf-8 -*-
import base64
import codecs

import scrapy
from scrapy.http import Response, Request
from scrapy.loader import ItemLoader

from ...items.ip import IPItem

__all__ = ('IpCoolproxySpider',)


class IpCoolproxySpider(scrapy.Spider):
    name = 'ip-coolproxy'
    allowed_domains = ['cool-proxy.net']
    start_urls = ['http://cool-proxy.net/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }

    def parse(self, response: Response):
        for row in response.css('table tr')[1:]:
            # 解密ip
            secret_ip = row.css('td:nth-child(1) script::text').re_first(
                r'rot13\(\"(.*?)\"'
            )
            if secret_ip is None:
                continue
            decoded_by_rot13 = codecs.decode(secret_ip, 'rot13')
            ip = base64.b64decode(decoded_by_rot13).decode()

            loader = ItemLoader(item=IPItem(), selector=row)
            loader.add_value('source', 'cool-proxy')
            loader.add_value('ip', ip)
            loader.add_value('protocol', 'http')
            loader.add_css('port', "td:nth-child(2)::text")
            loader.add_css('remark', 'td:nth-child(4)::text')

            yield loader.load_item()

        next_page = response.css('span.next a::attr("href")').extract_first()
        if next_page:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse
            )
