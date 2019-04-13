# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.loader import ItemLoader

from ..items.leiyang import LyCommunityPostItem, LyCommunityUserItem, LyCommunityCommentItem
from ..core.regexs import RE_DATETIME, RE_IMG_SRC

__all__ = ('LeiYangCommunitySpider',)


class LeiYangCommunitySpider(scrapy.Spider):
    name = 'leiyang-community'
    allowed_domains = ['www.lysq.com']

    def start_requests(self):
        forum_block_urls = {
            '纸都在线': 'http://www.lysq.com/forum-5-1.html',
        }
        for block_name, index_url in forum_block_urls.items():
            yield Request(
                index_url,
                callback=self.parse_forum_block_list,
                meta={'forum_block': block_name, 'page': 1}
            )

    def parse_forum_block_list(self, response: Response):
        post_list = response.css('table#threadlisttableid')
        post_urls = []

        for post in post_list.css('tbody[id!="separatorline"]'):
            loader = ItemLoader(item=LyCommunityPostItem(), selector=post)
            loader.add_value('block_name', response.meta['forum_block'])
            loader.add_css('title', 'a.s.xst::text')
            loader.add_css('url', 'a.s.xst::attr("href")')
            loader.add_css('author_username', 'td.by:nth-child(3) a::text')
            loader.add_css('created_time', 'td.by:nth-child(3) span::text')
            loader.add_css('last_comment_username', 'td.by:nth-child(5) a::text')
            loader.add_css('last_comment_time', 'td.by:nth-child(5) span::text')
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
                # 这个url是relative的, 并且是post的第一页, 所以不能使用response.url
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

    def parse_forum_post(self, response: Response):
        for floor, post_block in enumerate(response.css('#postlist div.postaaa'), start=1):
            # =============== 解析用户数据 =======================
            user_block = post_block.css('.favatar')
            username = user_block.css('.xw1::text').extract_first()
            user_loader = ItemLoader(item=LyCommunityUserItem(), selector=user_block)
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
            comment_loader = ItemLoader(item=LyCommunityCommentItem(), selector=comment_block)
            comment_loader.add_value('post_url', response.meta['post_url'])
            comment_loader.add_value('author_username', username)
            comment_loader.add_value('content', content)
            comment_loader.add_value('image_urls', content, re=RE_IMG_SRC)

            comment_header_loader = comment_loader.nested_css('div.pi')
            comment_header_loader.add_css('floor', 'strong em::text')
            comment_header_loader.add_value('floor', response.meta['page'] * 10 + floor)
            comment_header_loader.add_css('created_time', 'div.authi em::text', re=RE_DATETIME)

            yield comment_loader.load_item()