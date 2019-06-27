# -*- coding: utf-8 -*-
import re
import json

import scrapy
from scrapy.http import HtmlResponse, Request

from ...items.sanguo.hero import SanguoOlHeroItem

__all__ = ('SanguoOlSpider',)


class SanguoOlSpider(scrapy.Spider):
    name = 'sanguo-ol'
    allowed_domains = ['e3ol.com']
    LIST_API = 'http://www.e3ol.com/biography/inc_ajax.asp?types=index&pageno={page}'
    DETAIL_API = 'http://www.e3ol.com/biography/html/{name_url}/'

    def _process_dirty_json(self, response) -> dict:
        """这个接口返回的数据不是标准的JSON，需要处理之后才能解析

        - 字符串的最外面包含一堆括号，使用strip('()')去除
        - key两边没有引号，使用正则替换为它加上
        """
        body = response.body_as_unicode().strip('()')
        body = re.sub('([a-zA-Z0-9_]+):', r'"\1":', body)
        return json.loads(body)

    def start_requests(self):
        yield Request(
            url=self.LIST_API.format(page=1),
            callback=self.parse
        )

    def parse(self, response: HtmlResponse):
        json_resp = self._process_dirty_json(response)

        for hero in json_resp['soul']:
            yield SanguoOlHeroItem(
                name=hero['name'],
                pic=response.urljoin(hero['pic']),
                name_pinyin=hero['pinyin'],
                sex=hero['sex'],
                name_zi=hero['zi'],
                life_range=hero['shengsi'],
                come_from=hero['jiguan'],
                brief=hero['content'],
                cata=hero['cata']
            )

        if json_resp['page'] < json_resp['mpage']:
            yield response.follow(
                url=self.LIST_API.format(page=json_resp['page'] + 1),
                callback=self.parse
            )