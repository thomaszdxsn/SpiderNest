# -*- coding: utf-8 -*-
import re
from urllib.parse import urlencode
from datetime import datetime

import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse, XmlResponse
from scrapy.loader import ItemLoader

from SpiderNest.items.leiyang import LyCommunityPostItem, LyCommunityUserItem, LyCommunityCommentItem, Ly114Item
from SpiderNest.core.regexs import RE_DATETIME, RE_IMG_SRC

__all__ = ('LeiYangCommunitySpider', 'LeiyangCommnuity114Spider')


class LeiYangCommunitySpider(scrapy.Spider):
    name = 'leiyang-community'
    allowed_domains = ['www.lysq.com']
    start_urls = [
        'http://www.lysq.com/forum-5-1.html',
        'http://www.lysq.com/forum-6-1.html',
        'http://www.lysq.com/forum-114-1.html',
    ]

    def start_requests(self):
        forum_block_urls = {
            '纸都在线': 'http://www.lysq.com/forum-5-1.html',
            '社区水库': 'http://www.lysq.com/forum-6-1.html',
            '精彩活动': 'http://www.lysq.com/forum-114-1.html',
            '社区公益': 'http://www.lysq.com/forum-50-1.html',
            '微视自拍': 'http://www.lysq.com/forum-122-1.html',
            '旅游户外': 'http://www.lysq.com/forum-49-1.html',
            '原创文学': 'http://www.lysq.com/forum-35-1.html',
            '耒阳史记': 'http://www.lysq.com/forum-31-1.html',

        }
        for block_name, index_url in forum_block_urls.items():
            yield Request(
                index_url,
                callback=self.parse_forum_block_list,
                meta={'forum_block': block_name, 'page': 1}
            )

    def parse_forum_block_list(self, response: HtmlResponse):
        post_list = response.css('table#threadlisttableid')
        post_urls = []

        for post in post_list.css('tbody[id!="separatorline"]'):
            loader = ItemLoader(item=LyCommunityPostItem(), selector=post, base_url='http://www.lysq.com/')
            loader.add_value('block_name', response.meta['forum_block'])
            loader.add_css('title', 'a.s.xst::text')
            loader.add_css('url', 'a.s.xst::attr("href")')
            loader.add_css('author_username', 'td.by:nth-child(3) a::text')
            loader.add_css('created_time', 'td.by:nth-child(3) span::text')
            loader.add_css('last_comment_username', 'td.by:nth-child(5) a::text')
            loader.add_css('last_comment_time', 'td.by:nth-child(5) em span::attr("title")')
            loader.add_css('last_comment_time', 'td.by:nth-child(5) em span::text')
            loader.add_css('last_comment_time', 'td.by:nth-child(5) em a::text')
            loader.add_css('comment_count', 'td.num a::text')
            loader.add_css('view_count', 'td.num em::text')
            has_image = True if post.css('th.common img[alt="attach_img"]') else False
            loader.add_value('has_image', has_image)
            has_attachment = True if post.css('th.common img[alt="attachment"]') else False
            loader.add_value('has_attachment', has_attachment)

            item = loader.load_item()
            post_urls.append(item['url'])
            yield item

        for post_url in post_urls:
            yield Request(
                response.urljoin(post_url),
                callback=self.parse_forum_post,
                # 这个post_url是relative的, 并且是post的第一页, 所以不能使用response.url
                meta={'post_url': post_url, 'page': response.meta['page']}
            )

        next_page = response.css('div.pg a.nxt::attr("href")').extract_first()
        if next_page:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse_forum_block_list,
                meta={
                    **response.meta,
                    'page': response.meta['page'] + 1
                }
            )

    def parse_forum_post(self, response: HtmlResponse):
        for floor, post_block in enumerate(response.css('#postlist div.postaaa'), start=1):
            # =============== 解析用户数据 =======================
            user_block = post_block.css('.favatar')
            username = user_block.css('.xw1::text').extract_first()
            user_loader = ItemLoader(item=LyCommunityUserItem(), selector=user_block, base_url='http://www.lysq.com/')
            user_loader.add_value('username', username)
            user_loader.add_css('avatar_url', '.avtm img::attr("src")')
            user_loader.add_css('medal_list', 'p.md_ctrl img::attr("alt")')
            user_loader.add_css('coin_count', 'dl.pil dd::text', re='\d+')
            user_loader.add_css('user_group', 'a[href^="home.php?mod=spacecp&ac=usergroup"]::text')
            user_loader.add_css('signature', 'p.xg1::text')

            user_data_loader = user_loader.nested_css('div.tns')
            user_data_loader.add_css('topic_count', 'th:nth-child(1) a::text')
            user_data_loader.add_css('post_count', 'th:nth-child(2) a::text')
            user_data_loader.add_css('credit_count', 'td span::attr("title")')
            user_data_loader.add_css('credit_count', 'td a::text')

            yield user_loader.load_item()

            # =============== 解析post comment =================
            comment_block = post_block.css('td.plc')
            content = comment_block.css('.pcb .t_fsz').extract_first()
            comment_loader = ItemLoader(item=LyCommunityCommentItem(), selector=comment_block,
                                        base_url='http://www.lysq.com/')
            comment_loader.add_value('post_url', response.meta['post_url'])
            comment_loader.add_value('author_username', username)
            comment_loader.add_value('content', content)
            comment_loader.add_value('image_urls', content, re=RE_IMG_SRC)

            comment_header_loader = comment_loader.nested_css('div.pi')
            comment_header_loader.add_css('floor', 'strong em::text')
            comment_header_loader.add_value('floor', response.meta['page'] * 10 + floor)
            comment_header_loader.add_css('created_time', 'div.authi em::text', re=RE_DATETIME)
            yield comment_loader.load_item()


class LeiyangCommnuity114Spider(scrapy.Spider):
    name = 'leiyang-community-114'
    allowed_domains = ['www.lysq.com']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    _DETAIL_BODY_EXTRACT_PATTERN = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.M|re.U|re.DOTALL)
    _COMPANY_ID_EXTRACT_PATTERN = re.compile(r"rstblock\((\d+)\)")

    def _get_timestamp_for_now(self) -> int:
        return int(datetime.now().timestamp() * 1000)

    def _request_next_page(self, page: int, timestamp: int, formhash: str):
        params = {
            'id': 'xigua_114:xigua_114',
            'formhash': formhash,
            'inajax': '1',
            'page': page,
            '_': timestamp
        }
        base_url = 'http://www.lysq.com/plugin.php'
        url = f'{base_url}?{urlencode(params)}'
        yield Request(
            url,
            callback=self.parse,
            meta={'page': page, 'formhash': formhash}
        )

    def _request_detail_page(self, company_id: int, address: str, category: str):
        params = {
            'id': 'xigua_114',
            'mobile': 'no',
            'ac': 'profile',
            'company': company_id,
            'infloat': 'yes',
            'handlekey': 'xigua_114profile',
            'inajax': 1,
            'ajaxtarget': 'fwin_content_xigua_114profile'
        }
        base_url = 'http://www.lysq.com/plugin.php'
        url = f'{base_url}?{urlencode(params)}'
        yield Request(
            url,
            callback=self.parse_detail,
            meta={'address': address, 'category': category}
        )

    def start_requests(self):
        yield Request(
            url='http://www.lysq.com/plugin.php?id=xigua_114:xigua_114',
            callback=self.parse_index
        )

    def parse_index(self, response: HtmlResponse):
        # 需要破解discuz！的xss_check函数
        formhash = response.css('input[name="formhash"]::attr(value)').extract_first()
        yield from self._request_next_page(
            page=1,
            timestamp=self._get_timestamp_for_now(),
            formhash=formhash
        )

    def parse(self, response: HtmlResponse):
        if not response.body:
            # 如果response没有数据，代表已经爬取到了最大页数，停止爬取
            return

        for row in response.css('a.rstblock'):
            category = row.css('.rstblock-logo span::text').extract_first()
            address = row.css('.rstblock-content .rstblock-cost::text').extract()
            onclick_attr = row.css('::attr("onclick")').extract_first()
            company_id = self._COMPANY_ID_EXTRACT_PATTERN.match(onclick_attr).group(1)
            yield from self._request_detail_page(int(company_id), address, category)


        yield from self._request_next_page(
            page=response.meta['page'] + 1,
            timestamp=self._get_timestamp_for_now(),
            formhash=response.meta['formhash']
        )

    def parse_detail(self, response: XmlResponse):
        body = self._DETAIL_BODY_EXTRACT_PATTERN.search(response.body_as_unicode()).group()
        selector = Selector(text=body)
        loader = ItemLoader(item=Ly114Item(), selector=selector)

        loader.add_value('address', response.meta['address'])
        loader.add_value('category', response.meta['category'])
        loader.add_css('name', 'h1::text')
        loader.add_css('cover', 'img.logo::attr("src")')
        loader.add_css('description', 'div.rstblock-cost::text')
        loader.add_css('phone', 'span.rstblock-monthsales::text')
        # 微信号
        loader.add_css('wechat', 'label[onmouseover]::text')
        # 微信二维码
        loader.add_css('wechat', '#wechatqrlarge::attr("src")')
        loader.add_css('qq', 'a.qqtalk::text')

        yield loader.load_item()
