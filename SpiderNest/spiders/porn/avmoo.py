# -*- coding: utf-8 -*-
from collections import defaultdict

import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.loader import ItemLoader

from ...items.porn import AvmooActressItem, AvmooMovieItem

__all__ = ("AvmooSpider",)

# TODO: 403错误需要解决
class AvmooSpider(scrapy.Spider):
    name = 'avmoo'
    allowed_domains = ['avmoo.asia']
    start_urls = ['http://avmoo.asia/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'DOWNLOAD_DELAY': 2
    }

    def start_requests(self):
        yield Request(
            'https://avmoo.asia/cn/actresses',
            callback=self.parse_actresses_list
        )

        yield Request(
            'https://avmoo.asia/cn',
            callback=self.parse_movie_list,
        )

    def parse_actresses_list(self, response: HtmlResponse):
        for link in response.css('a.avatar-box::attr(href)'):
            yield response.follow(link, callback=self.parse_actress_detail_cn)

        next_page = response.css('ul.pagination a[name=nextpage]::attr(href)').extract_first(None)
        if next_page:
            yield response.follow(next_page, callback=self.parse_actresses_list)

    def parse_actress_detail_cn(self, response: HtmlResponse):
        loader = ItemLoader(item=AvmooActressItem(), selector=response)

        avatar_box = loader.nested_css('.avatar-box')
        avatar_box.add_css('avatar', 'img::attr(src)')
        avatar_box.add_css('name_cn', 'span::text')
        avatar_box.add_css('info', 'p::text')

        yield response.follow(
            response.url.replace('/cn/', '/en/'),
            callback=self.parse_actress_detail_en,
            meta={'item': loader.load_item()}
        )

    def parse_actress_detail_en(self, response: HtmlResponse):
        item = response.meta['item']
        item['name_en'] = response.css('.avatar-box span::text').extract_first()
        yield response.follow(
            response.url.replace('/en/', '/ja/'),
            callback=self.parse_actress_detail_jp,
            meta={'item': item}
        )

    def parse_actress_detail_jp(self, response: HtmlResponse):
        item = response.meta['item']
        item['name_jp'] = response.css('.avatar-box span::text').extract_first()
        yield AvmooActressItem(**item)

    def parse_movie_list(self, response: HtmlResponse):
        for link in response.css('#waterfall a.movie-box::attr(href)'):
            yield response.follow(
                link,
                callback=self.parse_movie_detail
            )

        next_page = response.css('ul.pagination a[name=nextpage]::attr(href)').extract_first(None)
        if next_page:
            yield response.follow(next_page, callback=self.parse_actresses_list)

    def parse_movie_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=AvmooMovieItem(), selector=response)

        loader.add_css('title', 'h3::text')
        loader.add_css('cover', 'a.bigImage img::attr(src)')
        loader.add_css('cast', '#avatar-waterfall a.avatar-box span::text')
        loader.add_css('stills', '#sample-waterfall img::attr(src)')

        INFO_NAME_MAPPING = {
            '识别码:': 'code',
            '发行时间:': 'publish_time',
            '长度:': 'time_length',
            '制作商:': 'create_vendor',
            '发行商:': 'publish_vendor',
            '类别:': 'categories',
            '导演:': 'director'
        }
        info_text = response.css('div.info *::text').extract()
        last_key = None
        info_dict = defaultdict(list)
        for raw_info in info_text:
            info = raw_info.strip()
            if not info:
                continue

            key = INFO_NAME_MAPPING.get(info, None)
            if key and key not in info_dict:
                last_key = key
                continue
            elif last_key is not None:
                info_dict[last_key].append(info)

        for k, v in info_dict.items():
            loader.add_value(k, v)

        yield loader.load_item()