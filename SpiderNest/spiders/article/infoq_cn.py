# -*- coding: utf-8 -*-
import json
from datetime import datetime
from typing import Optional

import scrapy
from scrapy.http import Response, Request

from ...core.utils import load_json_response
from ...items.article import InfoQCnArticleItem

__all__ = ("InfoQCnArticleItem",)


class InfoqCnSpider(scrapy.Spider):
    name = 'infoq-cn'
    allowed_domains = ['infoq.cn']
    _HEADERS = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'Accept-Language',
        'Content-Type': 'application/json',
        'Host': 'www.infoq.cn',
        'Origin': 'https://www.infoq.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    def __init__(self, *args, **kwargs):
        super(InfoqCnSpider, self).__init__(*args, **kwargs)
        self.mode = kwargs.pop('mode', 'full')
        self.update_max_page = kwargs.pop('update_max_page', 3)

    def _request_topic_info(self, topic_id: int):
        yield Request(
            'https://www.infoq.cn/public/v1/topic/getInfo',
            body=json.dumps({
                'id': topic_id
            }),
            method='POST',
            headers=self._HEADERS,
            callback=self.parse_topic_info
        )

    def _request_article_list(self, topic_id: int, page: int, score: Optional[int]=None):
        payload = {
            'id': topic_id,
            'size': 12,
            'type': 1,
        }
        if score:
            payload['score'] = score
        yield Request(
            'https://www.infoq.cn/public/v1/article/getList',
            body=json.dumps(payload),
            method='POST',
            headers=self._HEADERS,
            callback=self.parse_article_list,
            meta={'topic_id': topic_id, 'page': page}
        )

    def _request_article_detail(self, uuid: str):
        yield Request(
            'https://www.infoq.cn/public/v1/article/getDetail',
            body=json.dumps({
                'uuid': uuid
            }),
            method='POST',
            headers=self._HEADERS,
            callback=self.parse_article_detail
        )

    def start_requests(self):
        topic_id = 1
        yield from self._request_topic_info(topic_id)

    def parse_topic_info(self, response: Response):
        json_data = load_json_response(response)
        topic_id = json_data['data']['id']
        has_name = json_data['data']['name']

        if has_name:
            yield from self._request_article_list(topic_id, page=1)
        # topic id基本是500以内(目前在300以内, 2019.5.9)，中间可能会有跳跃
        if topic_id < 500 or has_name:
            yield from self._request_topic_info(topic_id=topic_id + 1)

    def parse_article_list(self, response: Response):
        json_data = load_json_response(response)
        data_list = json_data['data']
        if not data_list:
            return

        for item in data_list:
            yield from self._request_article_detail(item['uuid'])

        page = response.meta['page']
        if self.mode == 'update' and page > self.update_max_page:
            # 如果是增量爬取，只爬每个topic的前几页
            return

        yield from self._request_article_list(
            response.meta['topic_id'],
            page=page + 1,
            score=data_list[-1]['score']
        )

    def parse_article_detail(self, response: Response):
        json_data = load_json_response(response)
        data = json_data['data']
        yield InfoQCnArticleItem(
            cover=data['article_cover'],
            subtitle=data['article_subtitle'],
            summary=data['article_summary'],
            title=data['article_title'],
            author_names=[a['nickname'] for a in data['author']] if data['author'] else None,
            content=data['content'],
            publish_time=datetime.fromtimestamp(data['publish_time'] / 1000),
            topics=[t['name'] for t in data['topic']],
            uuid=data['uuid'],
            view_count=data['views'],
            url=response.url
        )
