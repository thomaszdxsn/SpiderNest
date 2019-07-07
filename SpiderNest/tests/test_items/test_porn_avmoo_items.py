import pytest
from scrapy.loader import ItemLoader

from ...items.porn.avmoo import AvmooActressItem, AvmooMovieItem
from ...models.porn.avmoo import AvmooActress, AvmooMovie


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


@pytest.mark.parametrize('params', [
{'cast': ['北川エリカ', '星奈あい', '一条みお', '皆月ひかる', '有栖るる', 'あゆみ莉花', '岬あずさ'],
 'categories': ['DMM独家', '荡妇', '放尿', '淫语', '主观视角', '高画质', '受虐男'],
 'code': ['DNJR-010'],
 'cover': ['https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010pl.jpg'],
 'create_vendor': ['犬/妄想族'],
 'director': ['肉糞亭ハラ美'],
 'publish_time': ['2019-08-04'],
 'publish_vendor': ['犬/妄想族'],
 'stills': ['https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-1.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-2.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-3.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-4.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-5.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-6.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-7.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-8.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-9.jpg',
            'https://jp.netcdn.space/digital/video/dnjr00010/dnjr00010-10.jpg'],
 'time_length': ['174分钟'],
 'title': ['DNJR-010 完全主観 貴方だけを見つめて尿道責め']},

{'cast': ['夏目彩春',
          '通野未帆',
          '成宮いろは',
          'たかせ由奈',
          '逢沢まりあ',
          '美谷朱里',
          '星川光希',
          '橋本れいか',
          '山岸琴音',
          '柴咲りか'],
 'categories': ['合集', '巨乳', 'DMM独家', '熟女', '已婚妇女', '数位马赛克', '4小时以上作品', '出轨'],
 'code': ['JUSD-839'],
 'cover': ['https://jp.netcdn.space/digital/video/jusd00839/jusd00839pl.jpg'],
 'create_vendor': ['マドンナ'],
 'publish_time': ['2019-08-03'],
 'publish_vendor': ['Madonna'],
 'time_length': ['480分钟'],
 'title': ['JUSD-839 義父のドス黒い肉棒と濃厚な愛撫でじっくりねっとり犯された美人妻 8時間']}
])
def test_AvmooMovieItem_processor(params):
    loader = ItemLoader(item=AvmooMovieItem())
    for k, v in params.items():
        loader.add_value(k, v)

    assert AvmooMovie(**loader.load_item())
