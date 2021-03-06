"""
author: thomaszdxsn
"""
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Identity

from ..processors import created_time_input_processor, populate_abs_url
from ..post import PostItem

__all__ = ('LyCommunityPostItem', 'LyCommunityUserItem', 'LyCommunityCommentItem', 'Ly114Item')


class LyCommunityPostItem(PostItem):
    author_username = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    block_name = Field(
        output_processor=TakeFirst()
    )
    comment_count = Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    has_attachment = Field(
        intput_processor=MapCompose(bool),
        output_processor=TakeFirst()
    )
    has_image = Field(
        input_processor=MapCompose(bool),
        output_processor=TakeFirst()
    )
    last_comment_time = Field(
        input_processor=MapCompose(str.strip, created_time_input_processor),
        output_processor=TakeFirst()
    )
    last_comment_username = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )


class LyCommunityUserItem(Item):
    username = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    avatar_url = Field(
        intput_processor=MapCompose(str, str.strip, populate_abs_url),
        output_processor=TakeFirst()
    )
    topic_count = Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    post_count = Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    credit_count = Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    coin_count = Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    medal_list = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Identity()
    )
    signature = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    user_group = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )


class LyCommunityCommentItem(Item):
    post_url = Field(
        input_processor=MapCompose(str, str.strip, populate_abs_url),
        output_processor=TakeFirst()
    )
    author_username = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    floor = Field(
        input_processor=MapCompose(int),
        output_processor=TakeFirst()
    )
    created_time = Field(
        input_processor=MapCompose(str.strip, created_time_input_processor),
        output_processor=TakeFirst()
    )
    content = Field(
        output_processor=TakeFirst()
    )
    signature = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    image_urls = Field(
        input_processor=MapCompose(str, str.strip, populate_abs_url),
        output_processor=Identity()
    )


class Ly114Item(Item):
    name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    address = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    category = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    cover = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    description = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    phone = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    # 微信有可能是微信ID，有可能是二维码
    wechat = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=lambda w: [i for i in w if i]
    )
    qq = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )