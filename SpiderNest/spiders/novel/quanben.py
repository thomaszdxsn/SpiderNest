# -*- coding: utf-8 -*-
import re
import time
from urllib.parse import urlencode

import scrapy
from scrapy.http import Request, FormRequest
from scrapy.loader import ItemLoader

from SpiderNest.items.novel.quanben import QuanbenBookItem, QuanbenBookChapterItem

__all__ = ('QuanbenXiaoshuoSpider',)


class QuanbenXiaoshuoSpider(scrapy.Spider):
    name = 'novel-quanben'
    start_urls = ['http://www.quanben.io/index.php?c=book&a=search&keywords=']
    _HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Host': 'www.quanben.io',
        'Referer': 'www.quanben.io',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3833.0 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    _CHAPTER_NAME_PATTERN = re.compile(r'^第\d+章?\s?(?P<chapter_name>.+)$')
    _AJAX_PARAMS_PATTERN = re.compile(r"""setTimeout
        \("ajax_post\(
        '(?P<c>\w+?)',
        '(?P<a>\w+?)',
        'pinyin',
        '(?P<pinyin>\w+)',
        'id',
        '(?P<id>\w+)',
        'sky',
        '(?P<sky>\w+)',
        't',
        '(?P<t>\w+?)'\)
    """, flags=re.VERBOSE)

    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse_book_list,
            headers=self._HEADERS
        )

    def parse_book_list(self, response):
        book_brief_urls = response.css('.box div.row a::attr(href)')

        for url in book_brief_urls:
            yield response.follow(
                url,
                callback=self.parse_book_brief,
                headers=self._HEADERS
            )

        next_page = response.css('p.page_next a::attr(href)').extract_first(None)
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_book_list,
                headers=self._HEADERS
            )

    def parse_book_brief(self, response):
        loader = ItemLoader(item=QuanbenBookItem(), selector=response)
        box = loader.nested_css('div.box')

        box.add_css('cover', 'img::attr(src)')
        box.add_css('name', 'h3 span::text')
        box.add_css('author_name', 'span[itemprop="author"]::text')
        box.add_css('category', 'span[itemprop="category"]::text')
        box.add_css('status', 'p:last-child span::text')
        box.add_css('brief', 'div.description *::text')
        item = loader.load_item()
        yield item

        chapter_list_url = response.css('div.box a.button.s1::attr(href)').extract_first()
        yield response.follow(
            chapter_list_url,
            callback=self.parse_chapter_list,
            headers=self._HEADERS,
            meta={'book_item': item}
        )

    def parse_chapter_list(self, response):
        chapter_elements = response.css('ul.list3 li')
        book_item = response.meta['book_item']

        for chapter_num, chapter_element in enumerate(chapter_elements, start=1):
            chapter_url = chapter_element.css('a::attr(href)').extract_first()
            chapter_name = chapter_element.css('a span::text').re_first(self._CHAPTER_NAME_PATTERN)
            yield response.follow(
                chapter_url,
                callback=self.parse_chapter_detail,
                meta={
                    'chapter_num': chapter_num,
                    'chapter_name': chapter_name,
                    'book_name': book_item['name'],
                    'book_author_name': book_item['author_name'],
                    'book_category': book_item['category']
                }
            )

    def parse_chapter_detail(self, response):
        ajax_params_raw = response.css('div#content + script::text').extract_first()
        params = self._AJAX_PARAMS_PATTERN.search(ajax_params_raw).groupdict()

        base_url = 'http://www.quanben.io/index.php'
        query_string_dict = {
            'c': params.pop('c'),
            'a': params.pop('a')
        }
        url = f'{base_url}?{urlencode(query_string_dict)}'
        post_params = {
            **params,
            '_type': 'ajax',
            'rndval': str(int(time.time() * 1000))
        }
        yield FormRequest(
            url,
            formdata=post_params,
            headers={
                **self._HEADERS,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            meta=response.meta,
            callback=self.parse_chapter_ajax_content
        )

    def parse_chapter_ajax_content(self, response):
        meta = response.meta
        loader = ItemLoader(item=QuanbenBookChapterItem())

        loader.add_value('content', response.body_as_unicode())
        loader.add_value('chapter_num', meta['chapter_num'])
        loader.add_value('chapter_name', meta['chapter_name'])
        loader.add_value('book_name', meta['book_name'])
        loader.add_value('book_author_name', meta['book_author_name'])
        loader.add_value('book_category', meta['book_category'])

        yield loader.load_item()
