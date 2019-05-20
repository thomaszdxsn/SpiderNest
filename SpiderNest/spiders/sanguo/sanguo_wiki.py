# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from ...items.sanguo.wiki import SanguoWikiCharacterItem
from ...core.regexs import RE_CHINESE

__all__ = ('SanguoWikiSpider',)


class SanguoWikiSpider(scrapy.Spider):
    name = 'sanguo-wiki'
    start_urls = ['http://san.nobuwiki.org/character']

    def parse(self, response: HtmlResponse):
        detail_urls = response.css('.excerpt h2 a::attr(href)').extract()
        for detail_url in detail_urls:
            yield response.follow(detail_url, callback=self.parse_detail)

        next_page = response.css('li.next-page a::attr(href)').extract_first(None)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=SanguoWikiCharacterItem(), selector=response)

        loader.add_css('name', 'h1 a::text', re=RE_CHINESE)
        loader.add_css('image', '.article-content img::attr(src)')
        loader.add_css('description', '.article-content *::text')
        loader.add_css('source', '.article-content .external::attr(href)', re='.+wikipedia.+')
        yield loader.load_item()
