# -*- coding: utf-8 -*-
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

    def start_requests(self):
        urls = [
            (EstateType.NEW, 'https://ly.513fm.com/house/'),
            (EstateType.SECOND_HAND, 'https://ly.513fm.com/sale/'),
            (EstateType.RENT, 'https://ly.513fm.com/rent/')
        ]
        for type_, url in urls:
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
        for link in response.css('ul.list li div.img a::attr("href")').extract():
            yield response.follow(link, callback=self._get_callback(type_))

        next_page = response.css('#aijiacms_next::attr("value")').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse, meta=response.meta)

    def parse_new(self, response: HtmlResponse) -> Iterator[LyEstateNewItem]:
        pass

    def parse_second_hand(self, response: HtmlResponse) -> Iterator[LyEstateSecondItem]:
        pass

    def parse_rent(self, response: HtmlResponse) -> Iterator[LyEstateRentItem]:
        pass