# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse, Request
from scrapy.loader import ItemLoader

from ...items.porn.x_art import XArtBlogPostItem, XArtModelItem, XArtVideoItem

__all__ = ('XArtSpider',)


class XArtSpider(scrapy.Spider):
    name = 'x-art'
    start_urls = ['https://www.x-art.com/models/order/popularity/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    _model_list_url = 'https://www.x-art.com/models/order/popularity/'
    _video_list_url = 'https://www.x-art.com/videos/'
    _blog_list_url = 'http://blog.x-art.com/'

    def start_requests(self):
        yield Request(
            self._model_list_url,
            callback=self.parse_model_list
        )

        yield Request(
            self._video_list_url,
            callback=self.parse_video_list
        )

        yield Request(
            self._blog_list_url,
            callback=self.parse_blog_list
        )

    def parse_model_list(self, response: HtmlResponse):
        detail_urls = response.css('#allmodels li a::attr(href)')
        for detail_url in detail_urls:
            yield response.follow(
                detail_url,
                callback=self.parse_model_detail,
            )

        links = response.css('.pagination li.arrow a::attr(href)').extract()
        if links:
            yield response.follow(
                links[-1],
                callback=self.parse_model_list
            )

    def parse_model_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=XArtModelItem(), selector=response)
        h2_texts = response.css('div.info h2::text').extract()

        loader.add_css('name', 'h1.show-for-large-up::text')
        loader.add_css('photo', 'img.info-img::attr(src)')
        loader.add_css('brief', 'div.info p::text')
        loader.add_value('vote_score', h2_texts[0])
        loader.add_value('vote_count', h2_texts[0])
        loader.add_value('age', h2_texts[2])
        loader.add_value('country', h2_texts[3])
        yield loader.load_item()

    def parse_video_list(self, response: HtmlResponse):
        detail_urls = response.css('#allvideos li a::attr(href)')
        for detail_url in detail_urls:
            yield response.follow(
                detail_url,
                callback=self.parse_video_detail,
            )

        links = response.css('.pagination li.arrow a::attr(href)').extract()
        if links:
            yield response.follow(
                links[-1],
                callback=self.parse_video_list
            )

    def parse_video_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=XArtVideoItem(), selector=response)
        h2_texts = response.css('h2::text').extract()
        vote_text = h2_texts[0]

        loader.add_css('name', 'div.info h1::text')
        loader.add_css('cover', 'div.widescreen img:not([class="start"])::attr(src)')
        loader.add_css('screenshots', 'div.gallery-item img::attr(src)')
        loader.add_css('cast', 'h2 a::text')
        loader.add_css('brief', 'p::text')
        loader.add_value('publish_time', h2_texts[2])
        loader.add_value('vote_count', vote_text)
        loader.add_value('vote_score', vote_text)
        yield loader.load_item()

    def parse_blog_list(self, response: HtmlResponse):
        detail_nodes = response.css('h2 a::attr(href)')
        for detail_node in detail_nodes:
            yield response.follow(detail_node, callback=self.parse_blog_detail)

        next_page = response.css('.next_page a::attr(href)').extract_first(None)
        if next_page:
            yield response.follow(next_page, callback=self.parse_blog_list)

    def parse_blog_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=XArtBlogPostItem(), selector=response)

        loader.add_css('title', 'div.blog_post_title h2::text')
        loader.add_css('content', 'article *::text')
        loader.add_css('like_count', '.like_count::text')
        loader.add_css('publish_time', '.listing_meta span:first-child::text')

        yield loader.load_item()