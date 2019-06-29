"""
author: thomaszdxsn
"""
from scrapy.loader import ItemLoader
import pytest

from ...items.porn.x_art import XArtModelItem, XArtVideoItem, XArtBlogPostItem
from ...models.porn.x_art import XArtModel, XArtVideo, XArtBlogPost


@pytest.mark.parametrize('params', [
    {'age': [' '],
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


@pytest.mark.parametrize('params', [
    {'brief': ['Try us out securely with Paypal ',
           '\r\n\n    ',
           'Katie and Isiah are totally in love,. They have been trying to '
           'work it out for a long time. But she is from UK and he’s from '
           'California. So as hard as they try, they just can’t seem to make '
           'the time difference make sense. The only issue is they have the '
           'HOTTEST sex that either has ever had!',
           '\xa0',
           'Every time they leave each other they come back and it’s better '
           'than before. Have you ever had this issue? Which to choose love or '
           'lust: or is it both? All I can say is this is one of the most '
           'real, raw sex scenes you will ever see!',
           '\xa0',
           'And this hot young couple cums hard! And Katie, Nympho that she '
           'is, must have 10 orgasms. If you want to learn how to please a '
           'woman, watch what Isiah does to Katie and watch her turn into an '
           'absolute animal right after a super romantic exchange.',
           '\xa0',
           'This happens in real life, right? xoxo Love, Colette',
           '\r\n\n                \r\n\n        ',
           '\r\n\n        ',
           '\r\n\n  ',
           '\r\n\n  ',
           '\r\n\n  ',
           '\r\n\n  '],
    'cast': ['Katie Jayne'],
    'cover': ['https://www.x-art.com/images_colette/simbolP.svg'],
    'name': ['In Love or Lust'],
    'publish_time': ['Jan 08, 2019 '],
    'screenshots': ['http://content1.x-art.com/videos/in_love_or_lust/x-art_isiah_katie '
                 'jayne_in_love_or_lust_3.jpg',
                 'http://content4.x-art.com/videos/in_love_or_lust/x-art_isiah_katie '
                 'jayne_in_love_or_lust_4.jpg',
                 'http://content2.x-art.com/videos/in_love_or_lust/x-art_isiah_katie '
                 'jayne_in_love_or_lust_5.jpg'],
    'vote_count': ['9.2 / 10 (739 votes)'],
    'vote_score': ['9.2 / 10 (739 votes)']},

    {'brief': ['Try us out securely with Paypal ',
           '\r\n\n    ',
           'Seth is busy working. And Nikki is feeling REALLY horny. She tries '
           "to excite him with her perfect body and sexy lingerie, but it's no "
           'use. Can you believe it?\xa0',
           'Lucky Nikki forgot she invited her HOT friend Charity over. She '
           'quickly gets Charity to agree to a threesome and strips her down '
           'to her panties.',
           "Now Seth decides to take notice. I mean isn't a threesome what "
           'every guy wants? And who could resist two of the hottest 22 year '
           'olds on the planet!',
           'So Seth goes from work, to working it. The girls climb on top and '
           'suck his cock. Then they take charge and take turns riding him. '
           'Finally he is hot and decides to participate. A LOT of steamy sex '
           'later and he cums all over them.',
           'Mission accomplished for Nikki. When in doubt, bring a friend. '
           'Remember that girls and guys. XOXO Colette\xa0',
           'PS. Lots more new models and new content comig. We finally have '
           'internet after the Malibu fires! The two new models here are Nikki '
           'Peaches and Charity Crawford',
           '\r\n\n                \r\n\n        ',
           '\r\n\n        ',
           '\r\n\n  ',
           '\r\n\n  ',
           '\r\n\n  ',
           '\r\n\n  '],
    'cover': ['https://www.x-art.com/images_colette/simbolP.svg'],
    'name': ['Three is NOT a Crowd'],
    'publish_time': ['Dec 20, 2018 '],
    'screenshots': ['http://content3.x-art.com/videos/three_is_not_a_crowd/x-art__three_is_not_a_crowd_3.jpg',
                 'http://content5.x-art.com/videos/three_is_not_a_crowd/x-art__three_is_not_a_crowd_4.jpg',
                 'http://content2.x-art.com/videos/three_is_not_a_crowd/x-art__three_is_not_a_crowd_5.jpg'],
    'vote_count': ['9.6 / 10 (730 votes)'],
    'vote_score': ['9.6 / 10 (730 votes)']}

])
def test_x_art_video_item(params):
    loader = ItemLoader(item=XArtVideoItem())
    for k, v in params.items():
        loader.add_value(k, v)

    assert XArtVideo(**loader.load_item())


@pytest.mark.parametrize('params', [
{'content': ['Here are a few “types” Kinky Aubrey, Baby Childhood Sweetheart, '
             'Connie large breasts older woman lover and Alex Untouchable '
             'Beauty Queen',
             'X-Art.com',
             ' to see more and more…',
             'Baby',
             '\xa0',
             'Connie',
             '\xa0and ',
             'alex and Aubrey',
             '\xa0so you can Join here; ',
             'X-Art.com/join\xa0',
             'for unlimited 4k downloads and streaming of thousands of movies '
             'and hundreds of thousands of photos that never expire or limit '
             'you with new updates all the time! BTW you can blow up your '
             'favorite erotic art by Brigham and hang it on your wall and save '
             'thousands (we do) Love, Colette',
             '\n',
             '\n'
             '\t\t\t#gallery-1 {\n'
             '\t\t\t\tmargin: auto;\n'
             '\t\t\t}\n'
             '\t\t\t#gallery-1 .gallery-item {\n'
             '\t\t\t\tfloat: left;\n'
             '\t\t\t\tmargin-top: 10px;\n'
             '\t\t\t\ttext-align: center;\n'
             '\t\t\t\twidth: 33%;\n'
             '\t\t\t}\n'
             '\t\t\t#gallery-1 img {\n'
             '\t\t\t\tborder: 2px solid #cfcfcf;\n'
             '\t\t\t}\n'
             '\t\t\t#gallery-1 .gallery-caption {\n'
             '\t\t\t\tmargin-left: 0;\n'
             '\t\t\t}\n'
             '\t\t\t/* see gallery_shortcode() in wp-includes/media.php */\n'
             '\t\t',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n',
             '\n'],
 'like_count': ['13'],
 'publish_time': ['January 13, 2017'],
 'title': ['Here are a few “types” Kinky Aubrey, Baby Childhood Sweetheart, '
           'Connie large breasts older woman lover and Alex Untouchable Beauty '
           'Queen']},

{'content': ['Happy SuperBowl Sunday from Franzi & Coco!',
             'Franziska used to be ',
             'Francesca',
             '\xa0one of our first and in my opinion best models and now '
             'directors we have ever had. She is smart, funny, gorgeous and '
             '(did I emphasize jaw-dropping gorgeous). That kind of beauty '
             'that ',
             'Caprice',
             '\xa0and ',
             'Jessica',
             '\xa0have.',
             '\n',
             'Now Franzi and I travel all over the world to find the most '
             'gorgeous girls who love to express themselves erotically. Check '
             'out our models and see if you can find one girl that wouldn’t '
             'make you drool all over a bar or turn your head away from the '
             'game today. Or girls (the commercials). A beautiful woman or an '
             'awesome game? Which do you choose?',
             '\n',
             'And off topic, before you judge our ',
             'models',
             '\xa0',
             'come inside and get to know them',
             '. They are so much more than beautiful faces and bodies.',
             '\n',
             'Happy Sunday,',
             '\n',
             'Love,',
             '\n',
             'Colette',
             '\n'],
 'like_count': ['52'],
 'publish_time': ['February 6, 2017'],
 'title': ['Happy SuperBowl Sunday from Franzi & Coco!']},

])
def test_x_art_blog_post_item(params):
    loader = ItemLoader(item=XArtBlogPostItem())
    for k, v in params.items():
        loader.add_value(k, v)

    assert XArtBlogPost(**loader.load_item())