# -*- coding: utf-8 -*-
import base64

import scrapy
from scrapy.http import Request, Response
from scrapy.loader import ItemLoader

from ...items.ip import IPItem


class ProxydbSpider(scrapy.Spider):
    name = 'ip-proxydb'
    allowed_domains = ['proxydb.net']
    start_urls = ['http://proxydb.net/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }

    def parse(self, response: Response):
        # 下面这个数字用来计算端口号
        data_num = response.css('html').re_first(
            r'<div style="display:none" data-[a-zA-Z]*="(\d+)"'
        )
        for tr in response.css('table.table-hover tbody tr'):
            loader = ItemLoader(item=IPItem(), selector=tr)
            loader.add_css('remark', 'td:nth-child(4) div::text')
            loader.add_css('protocol', 'td:nth-child(5)::text')

            # 解密IP
            script_elem = tr.css('td:nth-child(1) script::text')
            ip_first_part = script_elem.re_first(r'\'([\d\.]*)\'\.split')
            ip_first_part = ''.join(reversed(ip_first_part))

            hex_list = script_elem.re(r'\\x([A-Za-z0-9]{2})')
            b64_string = bytearray.fromhex(''.join(hex_list)).decode()
            ip_second_part = base64.b64decode(b64_string).decode()

            loader.add_value('ip', ip_first_part + ip_second_part)

            # 解密port
            raw_port = script_elem.re_first(r'var  pp =  \((\d+) -')
            loader.add_value('port', int(raw_port) + int(data_num))

            yield loader.load_item()