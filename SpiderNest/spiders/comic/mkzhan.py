# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from ...core.utils import load_json_response


class MkzhanSpider(scrapy.Spider):
    name = 'mkzhan'
    allowed_domains = ['mkzhan.com']
    COMIC_IDS = {
        '进击的巨人': '211879'
    }
    CHAPTER_LIST_BASE_URL = 'https://comic.mkzcdn.com/chapter/?comic_id={comic_id}'
    CHAPTER_BASE_URl = 'https://www.mkzhan.com/{comic_id}/{chapter_id}.html'

    def start_requests(self):
        for comic_name, comic_id in self.COMIC_IDS.items():
            url = self.CHAPTER_LIST_BASE_URL.format(comic_id=comic_id)
            yield Request(
                url,
                meta={'comic_name': comic_name, 'comic_id': comic_id},
                callback=self.parse_chapter_list
            )

    def parse_chapter_list(self, response):
        json_resp = load_json_response(response)
        for item in json_resp['data']:
            url = self.CHAPTER_BASE_URl.format(comic_id=response.meta['comic_id'], chapter_id=item['chapter_id'])
            yield Request(
                url,
                meta={**response.meta, **item},
                callback=self.parse
            )


    def parse(self, response):
        imgs = response.css('img.lazy-read::attr(data-src)').extract()

        yield {
            'imgs': imgs
        }



