# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from ...items.leiyang.ccoo import LyCcooRecruitmentItem
from ...core.regexs import RE_DATE

__all__ = ('LeiyangCcooRecruitSpider',)


class LeiyangCcooRecruitSpider(scrapy.Spider):
    name = 'leiyang-ccoo-recruit'
    allowed_domains = ['leiyang.ccoo.cn']
    start_urls = ['http://www.leiyang.ccoo.cn/post/zhaopin/']

    def __init__(self, *args, **kwargs):
        super(LeiyangCcooRecruitSpider, self).__init__(*args, **kwargs)
        self.pages = set()

    def parse(self, response: HtmlResponse):

        for row in response.css('ul.zhaopin-xx li'):
            detail_link = row.css('.mingqi01 span a::attr("href")').extract_first()
            if not detail_link:
                continue

            yield response.follow(detail_link, callback=self.parse_detail)

        links = response.css('div#page_x a::attr("href")').extract()
        for link in links:
            if link not in self.pages:
                self.pages.add(link)
                yield response.follow(link, callback=self.parse)

    def parse_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=LyCcooRecruitmentItem(), selector=response)

        loader.add_css('title', 'div.d_main h1::text')
        loader.add_css('publish_time', 'div.balefthead span:first-child::text', re=RE_DATE)
        loader.add_css('company_name', 'div.gongsimq::text')
        loader.add_css('company_info', 'div.gongsimq +p *::text')
        loader.add_css('company_description', 'div.gsjs *::text')
        loader.add_css('job_name', 'div.zpleftshow dd::text')
        loader.add_css('job_info', 'div.zpleftshow *::text')
        loader.add_css('job_description', 'div.zwms::text')

        yield loader.load_item()