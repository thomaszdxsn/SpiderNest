"""
author: thomaszdxsn
"""
import json
from ....spiders.article.infoq_cn import InfoqCnSpider, InfoQCnArticleItem


def test_infoq_cn_spider(resource_post):
    spider = InfoqCnSpider()
    headers = spider._HEADERS
    start_request = next(spider.start_requests())

    topic_response = resource_post(start_request.url, json=json.loads(start_request.body),
                                   request=start_request, headers=headers)
    topic_parse = spider.parse_topic_info(topic_response)
    article_list_request = next(topic_parse)

    article_list_response = resource_post(article_list_request.url, json=json.loads(article_list_request.body),
                                          request=article_list_request, headers=headers)
    list_parse = spider.parse_article_list(article_list_response)
    detail_request = next(list_parse)

    detail_response = resource_post(detail_request.url, json=json.loads(detail_request.body),
                                    request=detail_request, headers=headers)
    detail_parse = spider.parse_article_detail(detail_response)
    detail_result = list(detail_parse)
    assert len(detail_result) > 0

    for result in detail_result:
        assert isinstance(result, InfoQCnArticleItem)



