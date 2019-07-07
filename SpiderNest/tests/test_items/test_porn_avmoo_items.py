import pytest
from scrapy.loader import ItemLoader

from ...items.porn.avmoo import AvmooActressItem
from ...models.porn.avmoo import AvmooActress


@pytest.mark.parametrize('params', [
{'avatar': ['https://jp.netcdn.space/mono/actjpgs/mari_rika.jpg'],
 'info': ['生日: 1993-06-09',
          '年龄: 26',
          '身高: 148cm',
          '罩杯: D',
          '胸围: 80cm',
          '腰围: 56cm',
          '臀围: 82cm',
          '爱好: ゲーム(RPG)、映画'],
 'name_cn': ['麻里梨夏'],
 'name_en': ['Rika Mari'],
 'name_jp': ['麻里梨夏']},

{'avatar': ['https://jp.netcdn.space/mono/actjpgs/ootuki_hibiki.jpg'],
 'info': ['生日: 1988-02-21',
          '年龄: 31',
          '身高: 162cm',
          '罩杯: E',
          '胸围: 88cm',
          '腰围: 57cm',
          '臀围: 85cm',
          '出生地: 北海道'],
 'name_cn': ['大槻ひびき'],
 'name_en': ['Hibiki Otsuki'],
 'name_jp': ['大槻ひびき']},

{'avatar': ['https://jp.netcdn.space/mono/actjpgs/atomi_syuri.jpg'],
 'info': ['身高: 156cm', '胸围: 85cm', '腰围: 55cm', '臀围: 85cm', '爱好: 釣り、絵を描くこと'],
 'name_cn': ['跡美しゅり'],
 'name_en': ['Shuri Atomi'],
 'name_jp': ['跡美しゅり']}
])
def test_AvmooActressItem_processor(params):
    loader = ItemLoader(item=AvmooActressItem())
    for k, v in params.items():
        loader.add_value(k, v)
    assert AvmooActress(**loader.load_item())
