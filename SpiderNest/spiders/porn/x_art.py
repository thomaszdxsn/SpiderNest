# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse, Request
from scrapy.loader import ItemLoader

from ...items.porn.x_art import XArtBlogPostItem, XArtModelItem, XArtVideoItem

__all__ = ('XArtSpider',)


class XArtSpider(scrapy.Spider):
    name = 'x-art'
    allowed_domains = ['x-art.com']
    start_urls = ['https://www.x-art.com/models/order/popularity/']

    def start_requests(self):
        model_list_url = 'https://www.x-art.com/models/order/popularity/'
        yield Request(
            model_list_url,
            callback=self.parse_model_list
        )

        video_list_url = 'https://www.x-art.com/videos/'
        yield Request(
            video_list_url,
            callback=self.parse_video_list
        )

        blog_list_url = 'http://blog.x-art.com/'
        yield Request(
            blog_list_url,
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
        # yield loader.load_item()

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
        loader.add_css('cover', 'div.widescreen img[class$="start"]::attr(src)')
        loader.add_css('screenshots', 'div.gallery-item img::attr(src)')
        loader.add_css('cast', 'h2 a::text')
        loader.add_css('brief', 'p::text')
        loader.add_value('publish_time', h2_texts[2])
        loader.add_value('vote_count', vote_text)
        loader.add_value('vote_score', vote_text)
        yield loader.load_item()

    def parse_blog_list(self, response: HtmlResponse):
        pass