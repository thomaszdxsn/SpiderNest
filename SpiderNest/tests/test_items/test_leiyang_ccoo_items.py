"""
author: thomaszdxsn
"""
import pytest
from scrapy.loader import ItemLoader

from ...items.leiyang.ccoo import construct_info, replace_cn_punc, LyCcooRecruitmentItem
from ...models.leiyang.ccoo import LyCcooRecruitmentInfo


@pytest.mark.parametrize('arg', [
    [
     '', '', '招聘职位', '', '业务/销售', '', '招聘人数', '', '5人', '',
     '公司地址', '', '[市区]东莞市南城区第一国际汇一城1510-1511', '', '联 系 人', '', '陈先生', '', 'ＱＱ交谈', '', '', '', ''
    ],
])
def test_construct_info_out_processor(arg):
    output = construct_info(arg)
    assert isinstance(output, dict)


@pytest.mark.parametrize('arg,expect', [
    ('联 系 人', '联系人'),
    ('招聘职位：', '招聘职位')
])
def test_replace_cn_punc_in_processor(arg, expect):
    output = replace_cn_punc(arg)
    assert output == expect


def test_ly_ccoo_recruitment_item():
    raw_data = {
        'company_description': ['\r\n          ',
                                '公司名称：\r\n            珠江精品瓷砖\r\n            ',
                                '\r\n            公司地址：体育中路178号 ',
                                '\r\n            公司行业：-- ',
                                '\r\n            公司类型：-- ',
                                '\r\n            公司规模：-- ',
                                '\r\n          中高端瓷砖',
                                '\r\n        '],
        'company_info': ['公司规模：', '-- ', '公司性质：', '-- ', '公司行业：', '-- '],
        'company_name': ['\r\n              珠江精品瓷砖\r\n              ',
                         '\r\n              \r\n            '],
        'job_description': ['勤奋，踏实！\r\n        '],
        'job_info': ['\r\n            ',
                     '\r\n              ',
                     '招聘职位：',
                     '\r\n              ',
                     '业务/销售',
                     '\r\n              ',
                     '招聘人数：',
                     '\r\n              ',
                     '1人',
                     '\r\n              ',
                     '公司地址：',
                     '\r\n              ',
                     '[市区]体育中路178号',
                     '\r\n              ',
                     '联 系 人：',
                     '\r\n              ',
                     '吴伟峰',
                     '\r\n              ',
                     'ＱＱ交谈：',
                     '\r\n              ',
                     '-- ',
                     '\r\n            ',
                     '\r\n          '],
        'job_name': ['业务/销售', '1人', '[市区]体育中路178号', '吴伟峰', '-- '],
        'publish_time': ['2018-10-13'],
        'title': ['新中源珠江精品瓷砖招聘业务员数名']
    }
    loader = ItemLoader(item=LyCcooRecruitmentItem())
    for k, v in raw_data.items():
        loader.add_value(k, v)
    item = loader.load_item()
    assert LyCcooRecruitmentInfo(**item)
