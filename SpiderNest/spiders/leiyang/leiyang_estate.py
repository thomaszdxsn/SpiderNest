# -*- coding: utf-8 -*-
import re
from typing import Callable, Iterator

import scrapy
from scrapy.http import HtmlResponse, Request
from scrapy.loader import ItemLoader

from ...items.leiyang.estate import (
    LyEstatePostItem, LyEstateNewItem,
    LyEstateRentItem, LyEstateSecondItem
)
from ...items.estate import EstateType
from ...core.regexs import RE_DATE

__all__ = ("LyEstateInfoSpider", "LyEstatePostSpider")


class LyEstatePostSpider(scrapy.Spider):
    name = 'leiyang-estate-post'
    allowed_domains = ['513fm.com']
    start_urls = [
        'https://ly.513fm.com/news/list-28.html',
        'https://ly.513fm.com/news/list-29.html',
        'https://ly.513fm.com/news/list-31.html'
    ]

    def parse(self, response: HtmlResponse):

        for detail_link in response.css('.list-wrap a::attr("href")'):
            yield response.follow(detail_link, callback=self.parse_detail)

        next_page = response.css('#aijiacms_next::attr("value")').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=LyEstatePostItem(), selector=response)

        loader.add_css('title', 'h1+p::text')
        loader.add_css('author', '.title_sm span:nth-child(1)', re='来源：(.*?)</')
        loader.add_css('created_time', '.title_sm span:nth-child(2)', re=RE_DATE)
        loader.add_css('view_count', '#hits::text')
        loader.add_css('content', '#content *::text')
        loader.add_css('brief', '.news_zy p::text')
        loader.add_value('url', response.url)

        yield loader.load_item()


class LyEstateInfoSpider(scrapy.Spider):
    name = 'leiyang-estate-info'
    allowed_domains = ['513fm.com']
    urls = dict([
        (EstateType.NEW, 'https://ly.513fm.com/house/'),
        (EstateType.SECOND_HAND, 'https://ly.513fm.com/sale/'),
        (EstateType.RENT, 'https://ly.513fm.com/rent/')
    ])
    _INFO_PATTERN = re.compile(r'：(.+)', flags=re.UNICODE)

    def start_requests(self):
        for type_, url in self.urls.items():
            yield Request(url, callback=self.parse, meta={'type': type_})

    def _get_callback(self, type_: EstateType) -> Callable:
        if type_ == EstateType.NEW:
            return self.parse_new
        elif type_ == EstateType.SECOND_HAND:
            return self.parse_second_hand
        elif type_ == EstateType.RENT:
            return self.parse_rent
        raise ValueError('不支持其它类型')

    def parse(self, response: HtmlResponse) -> Iterator[Request]:
        type_ = response.meta['type']
        for link in response.css('ul h3 a::attr("href")').extract():
            yield response.follow(link, callback=self._get_callback(type_))

        next_page = response.css('#aijiacms_next::attr("value")').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta=response.meta)

    def parse_new(self, response: HtmlResponse) -> Iterator[Request]:
        loader = ItemLoader(item=LyEstateNewItem(), selector=response)

        loader.add_css('title', 'h1 a::text')
        loader.add_css('tags', '.house_name h3 a::text')
        loader.add_css('price_per_square', '.js li:nth-child(1) span::text')
        loader.add_css('main_styles', '.js li:nth-child(5) div.fl::text')
        loader.add_css('developer', '.js li:nth-child(5) div.fr::text')
        loader.add_css('project_type', '.js li:nth-child(6) div.fl::text')
        loader.add_css('decoration', '.js li:nth-child(6) div.fr::text')
        loader.add_css('address', '.js li:nth-child(7).more::text')
        loader.add_css('marketing_address', '.js li:nth-child(8).more::text')

        item = loader.load_item()
        desc_url = "https:" + response.css('#house_nav li:nth-child(2) a::attr("href")').extract_first()
        yield Request(
            desc_url,
            callback=self.parse_new_description,
            meta={'item': item}
        )

    def parse_new_description(self, response: HtmlResponse) -> Iterator[LyEstateNewItem]:
        loader = ItemLoader(item=response.meta['item'], selector=response)
        loader.add_css('description', '.detail_fl *::text')
        yield loader.load_item()

    def parse_second_hand(self, response: HtmlResponse) -> Iterator[LyEstateSecondItem]:
        loader = ItemLoader(item=LyEstateSecondItem(), selector=response)

        loader.add_css('title', 'h1::text')
        loader.add_css('price', 'td span.red *::text')

        info_loader = loader.nested_css('.dtl_frinfo table')
        info_loader.add_css('area', 'tr:nth-child(2) td:nth-child(1)::text', re='\d+')
        info_loader.add_css('style', 'tr:nth-child(2) td:nth-child(2)::text', re=self._INFO_PATTERN)
        info_loader.add_css('direction', 'tr:nth-child(3) td:nth-child(1)::text', re=self._INFO_PATTERN)
        info_loader.add_css('floor', 'tr:nth-child(3) td:nth-child(2)::text', re=self._INFO_PATTERN)
        info_loader.add_css('house_type', 'tr:nth-child(4) td:nth-child(1) a::text')
        info_loader.add_css('decoration', 'tr:nth-child(4) td:nth-child(2)::text', re=self._INFO_PATTERN)
        info_loader.add_css('age', 'tr:nth-child(5) td::text', re=self._INFO_PATTERN)
        info_loader.add_css('address', 'tr:nth-child(7) td::text', re=self._INFO_PATTERN)

        loader.add_css('description', '.dtl_content *::text')
        loader.add_css('images', '.dtl_pics img::attr("src")')

        yield loader.load_item()


    def parse_rent(self, response: HtmlResponse) -> Iterator[LyEstateRentItem]:
        loader = ItemLoader(item=LyEstateRentItem(), selector=response)

        loader.add_css('title', 'h1::text')

        info_loader = loader.nested_css('.dtl_frinfo')
        info_loader.add_css('per_month_price', 'tr:nth-child(1) b::text')
        info_loader.add_css('area', 'tr:nth-child(2) td:nth-child(1)::text', re='\d+')
        info_loader.add_css('style', 'tr:nth-child(2) td:nth-child(2)::text', re=self._INFO_PATTERN)
        info_loader.add_css('direction', 'tr:nth-child(3) td:nth-child(1)::text', re=self._INFO_PATTERN)
        info_loader.add_css('floor', 'tr:nth-child(3) td:nth-child(2)::text', re=self._INFO_PATTERN)
        info_loader.add_css('house_type', 'tr:nth-child(4) td:nth-child(1) a::text')
        info_loader.add_css('decoration', 'tr:nth-child(4) td:nth-child(2)::text', re=self._INFO_PATTERN)
        info_loader.add_css('age', 'tr:nth-child(5) td::text', re=self._INFO_PATTERN)
        info_loader.add_css('address', 'tr:nth-child(7) td::text', re=self._INFO_PATTERN)

        loader.add_css('description', '.dtl_content *::text')
        loader.add_css('images', '.dtl_pics img::attr("src")')

        yield loader.load_item()