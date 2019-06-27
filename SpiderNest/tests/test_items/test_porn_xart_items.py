"""
author: thomaszdxsn
"""
from scrapy.loader import ItemLoader
import pytest

from ...items.porn.x_art import XArtModelItem, XArtVideoItem, XArtBlogPostItem
from ...models.porn.x_art import XArtModel


@pytest.mark.parametrize('params', [
    {'age': [' 20'],
    'brief': ['\r\n'
           '\n'
           '    Petite Leah Gotti is stunning with her red hair, green eyes '
           "and a fuck-me-now attitude that both men and women love. Don't let "
           'her adorable good looks and youth fool you. This college coed is '
           'an accomplished swimmer and gymnast who knows exactly how to use '
           "her athletic body to give and receive total pleasure. And here's a "
           'bonus for you guys: Most girls like sucking cock, but Leah '
           'absolutely loves it. This teenager already has a deep throat '
           'technique that can make any man explode. Practice makes perfect, '
           'and Leah is known to partake in the occasional Gang Bang with '
           'multiple guys when she feels like it. And her tender sexuality '
           'when licking pussy is something to behold. Wish they all could be '
           'California Girls like Leah.    '],
    'country': [' USA'],
    'name': ['Leah Gotti'],
    'photo': ['http://content3.x-art.com/models/leah_gotti/x-art_leah_gotti-01-lrg.jpg'],
    'vote_count': ['9.4 / 10 (372 votes)'],
    'vote_score': ['9.4 / 10 (372 votes)']},

    {'age': [' 19'],
     'brief': ['\r\n'
               '\n'
               '    With her beautiful facial features, those perfect 34D cup '
               'tits, and an ass that would stop traffic, Milla is destined to be '
               'a super star. Her playfulness and positive outlook on life and '
               'love makes this Ukrainian girl a joy on the set. Trust me, Mila '
               "loves to tease. It doesn't hurt that brown-eyed Milla is "
               'completely comfortable getting naked and is a very sensual, '
               'intelligent woman. She loves to play with her clit and to '
               'finger-fuck herself to earth-shaking orgasms. "It is true," Milla '
               'says. "I do masturbate every day.  Unless," she adds with that '
               'beguiling smile, "I get a better offer. Would X-Art subscribers '
               'like to see that?" Some questions answer themselves!    '],
     'country': [' Ukraine'],
     'name': ['Milla'],
     'photo': ['http://content4.x-art.com/models/milla/x-art_milla-01-lrg.jpg'],
     'vote_count': ['9.5 / 10 (559 votes)'],
     'vote_score': ['9.5 / 10 (559 votes)']}
])
def test_x_art_model_item(params):
    loader = ItemLoader(item=XArtModelItem())
    for k, v in params.items():
        loader.add_value(k, v)

    assert XArtModel(**loader.load_item())