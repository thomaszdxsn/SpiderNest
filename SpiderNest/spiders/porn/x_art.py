# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse, Request


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
                callback=self.parse
            )

    def parse_model_detail(self, response: HtmlResponse):
        pass

    def parse_video_list(self, response: HtmlResponse):
        pass

    def parse_blog_list(self, response: HtmlResponse):
        pass