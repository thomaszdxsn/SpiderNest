# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from ...items.leiyang.rencai import LyRencaiRecruitmentItem, LyRencaiCompanyItem
from ...core.regexs import RE_DATE

__all__ = ('LeiyangVhCompanySpider', 'LeiyangVhJobSpider')


class LeiyangVhJobSpider(scrapy.Spider):
    name = 'lyvh-job'
    allowed_domains = ['lyvh.com']
    start_urls = ['http://www.lyvh.com/job/']

    def parse(self, response: HtmlResponse):

        for row in response.css('div.search_job_list'):
            company_name = row.css('div.search_job_com_t_name a::text').extract_first()
            detail_href = row.css('div.search_user_list_neme a::attr("href")').extract_first()

            yield response.follow(
                detail_href,
                callback=self.parse_detail,
                meta={'company_name': company_name}
            )

        pages = response.css('.pages a::attr("href")').extract()
        if pages:
            next_page = pages[-1]
            if next_page != response.url:
                yield response.follow(
                    next_page,
                    callback=self.parse
                )

    def parse_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=LyRencaiRecruitmentItem(), selector=response)

        loader.add_value('company_name', response.meta['company_name'])
        loader.add_css('title', 'h1::text')
        loader.add_css('salary', '.Company_Basic_information_xz::text')
        loader.add_css('publish_time', '.Company_post_State_s::text', re=RE_DATE)
        loader.add_css('requirements', '.Company_Basic_information_l::text')
        loader.add_css('tags', 'div.Company_Basic_information_r span.yun_com_fl_dy_cor::text')
        loader.add_css('description', '.Job_Description *::text')

        yield loader.load_item()


class LeiyangVhCompanySpider(scrapy.Spider):
    name = 'lyvh-company'
    allowed_domains = ['lyvh.com']
    start_urls = ['http://www.lyvh.com/company/']

    def parse(self, response: HtmlResponse):
        for detail_url in response.css('.firm_list div.firm_list_logo a::attr("href")'):
            yield response.follow(detail_url, callback=self.parse_detail)

        next_page = response.css('.pages a::attr("href")')[-1].extract()
        if next_page != response.url:
            yield response.follow(
                next_page,
                callback=self.parse
            )

    def parse_detail(self, response: HtmlResponse):
        loader = ItemLoader(item=LyRencaiCompanyItem(), selector=response)

        loader.add_css('name', 'h1::text')
        loader.add_css('cover', '.com_show_toplogo img::attr("src")')
        loader.add_css('tags', '.com_show_cominfo span::text')
        loader.add_css('description', 'div.con_show_introduction p.MsoNormal::text')

        yield loader.load_item()