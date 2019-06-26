"""
author: thomaszdxsn
"""
from SpiderNest.spiders.leiyang.leiyang_vh import LeiyangVhCompanySpider, LeiyangVhJobSpider
from SpiderNest.items.leiyang.rencai import LyRencaiCompanyItem, LyRencaiRecruitmentItem
from SpiderNest.models.leiyang.rencai import LyRencaiCompanyInfo, LyRencaiJobInfo


def test_leiyang_rencaiweb_job_spider(resource_get):
    spider = LeiyangVhJobSpider()

    start_response = resource_get(spider.start_urls[0])
    parse_results = spider.parse(start_response)
    detail_request = next(parse_results)

    detail_response = resource_get(detail_request.url, request=detail_request)
    detail_results = list(spider.parse_detail(detail_response))
    assert len(detail_results) > 0

    for result in detail_results:
        assert isinstance(result, LyRencaiRecruitmentItem)
        assert LyRencaiJobInfo(**result)


def test_leiyang_recaiweb_company_spider(resource_get):
    spider = LeiyangVhCompanySpider()

    start_response = resource_get(spider.start_urls[0])
    parse_results = spider.parse(start_response)
    detail_request = next(parse_results)

    detail_response = resource_get(detail_request.url, request=detail_request)
    detail_results = list(spider.parse_detail(detail_response))
    assert len(detail_results) > 0

    for result in detail_results:
        assert isinstance(result, LyRencaiCompanyItem)
        assert LyRencaiCompanyInfo(**result)