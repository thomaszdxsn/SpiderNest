"""
author: thomaszdxsn
"""
import datetime

import pytest
from scrapy.loader import ItemLoader

from ...items.leiyang.rencai import LyRencaiRecruitmentItem, LyRencaiCompanyItem
from ...models.leiyang.rencai import LyRencaiJobInfo, LyRencaiCompanyInfo


@pytest.mark.parametrize('params', [
{'company_name': '蓉兴母婴连锁',
 'description': [' 1.协助财务相关工作\n2.与门店紧密配合，协调沟通\n3.相关销售资料整理、编制\n4.熟练掌握办公软件 '],
 'publish_time': '2019-05-09',
 'salary': ['面议'],
 'title': '办公室文员'},

{'company_name': '蓉兴母婴连锁',
 'description': [' 1.有零售行业或卖场管理工作经验,有良好的沟通技巧，与团队管理能力\n'
                 '2.熟练掌握门店管理的各项规范和操作方法，对事物有较强的分析和决策能力\n'
                 '3.有一定的店铺运营策划能力，全面负责店内的日常工作，具有责任感，善于调动员工的积极性，提升门店服务质量\n'
                 '4.电脑操作熟练，擅长使用办公软件 '],
 'publish_time': '2019-05-08',
 'salary': ['￥4000-10000'],
 'title': '运营'},
])
def test_ly_rencei_recruit_item_processor_is_valid(params):
    loader = ItemLoader(item=LyRencaiRecruitmentItem())
    for k, v in params.items():
        loader.add_value(k, v)
    item = loader.load_item()
    assert LyRencaiJobInfo(**item)


@pytest.mark.parametrize('params', [
{'cover': ['http://www.lyvh.com/data/logo/20170418/14906489056.PNG'],
 'description': ['\r\n\t耒阳市京之东装饰工程',
                 ' ',
                 '2010年，品牌名为：京东',
                 '2017年迁往盛世华城2000平米办公新址，同时正式升级为京东',
                 '2012年以来用产值遥遥领先同行的增长速度再次证明了家博竞争实力，家博的成功引发了全行业的思考和跟进，每年都吸引大量省内外装修企业来参观和学习。 ',
                 ' \r\n',
                 '\r\n\t京东装饰工程有限公司是集基材、主材、家具、家电，软装',
                 ',公司以全心全意为人居服务的宗旨,打造中国真正意义上的一站式服务体系,让普通百姓花更少的钱搬进自己更心仪的家。\r\n'],
 'name': ['耒阳京之东装饰工程有限公司   '],
 'tags': ['家居/室内设计/装潢', '湖南 ', '个体 ', '50-200人 ', '注资80万 ', '2019-04创办']},

{'cover': ['http://www.lyvh.com/data/upload/company/20190425/1556173860755_1.PNG'],
 'name': ['欧美达家居   '],
 'tags': ['家居/室内设计/装潢', '湖南 ', '个体 ', '50-200人 ', '注资1000万 ', '2000创办']}
])
def test_ly_rencai_company_item_processor_is_valid(params):
    loader = ItemLoader(item=LyRencaiCompanyItem())
    for k, v in params.items():
        loader.add_value(k, v)
    item = loader.load_item()
    assert LyRencaiCompanyInfo(**item)