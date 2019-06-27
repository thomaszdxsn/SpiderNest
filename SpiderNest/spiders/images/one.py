# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.loader import ItemLoader

from ...items.one import OneImgItem

__all__ = ('OneSpider',)


class OneSpider(scrapy.Spider):
    name = 'one'
    allowed_domains = ['wufazhuce.com']
    start_urls = ['http://wufazhuce.com/']
    _URL_INDEX_MATCH = re.compile(r'/(\d+)$')
    _BASE_IMG_URL = 'http://wufazhuce.com/one/{index}'
    _BASE_ARTICLE_URL = 'http://wufazhuce.com/article/{index}'
    _BASE_QUESTION_URL = 'http://wufazhuce.com/question/{index}'

    def __init__(self, *args, **kwargs):
        super(OneSpider, self).__init__(*args, **kwargs)
        self.img_start_index = 1
        self.article_start_index = 1
        self.question_start_index = 1

    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse_index
        )

    def parse_index(self, response: HtmlResponse):
        img_max_index = int(response.css('#carousel-one a::attr(href)').re_first(self._URL_INDEX_MATCH))
        for i in range(self.img_start_index, img_max_index + 1):
            yield response.follow(
                self._BASE_IMG_URL.format(index=i),
                callback=self.parse_img
            )

        # article_max_index = int(response.css('.fp-one-articulo ul li a::attr(href)').re_first(self._URL_INDEX_MATCH))
        # for i in range(self.article_start_index, article_max_index + 1):
        #     yield response.follow(
        #         self._BASE_ARTICLE_URL.format(index=i),
        #         callback=self.parse_article
        #     )
        #
        # question_max_index = int(response.css('.fp-one-cuestion ul li a::attr(href)').re_first(self._URL_INDEX_MATCH))
        # for i in range(self.question_start_index, question_max_index + 1):
        #     yield response.follow(
        #         self._BASE_QUESTION_URL.format(index=i),
        #         callback=self.parse_question
        #     )

    def parse_img(self, response: HtmlResponse):
        loader = ItemLoader(item=OneImgItem(), selector=response)

        loader.add_css('image', '.one-imagen img::attr(src)')
        loader.add_css('title', '.one-titulo::text')
        loader.add_css('proverb', '.one-cita::text')
        loader.add_css('date', '.one-pubdate *::text')

        yield loader.load_item()

    def parse_article(self, response: HtmlResponse):
        pass

    def parse_question(self, response: HtmlResponse):
        pass
