"""
author: thomaszdxsn
"""
import pytest
from scrapy.loader import ItemLoader

from SpiderNest.items.sanguo.wiki import SanguoWikiCharacterItem
from SpiderNest.models.sanguo.wiki import SanguoWikiCharacter


@pytest.mark.parametrize('params', [
    {'description': [' ',
                 '呂凱',
                 ' ',
                 'Lu Kai',
                 '（生沒年不詳），字季平，永昌郡不韋縣（今雲南保山東北）人，蜀漢官員。',
                 ' ',],
     'image': ['http://san.nobuwiki.org/pic/character_san/0155.jpg'],
     'name': ['呂岱'],
     }

])
def test_sanguo_wiki_character_item(params):
    loader = ItemLoader(item=SanguoWikiCharacterItem())

    for k, v in params.items():
        loader.add_value(k, v)

    assert SanguoWikiCharacter(**loader.load_item())
