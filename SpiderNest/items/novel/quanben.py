from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Join

__all__ = ('QuanbenBookItem', 'QuanbenBookChapterItem')


class QuanbenBookItem(Item):
    cover = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    category = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    author_name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    status = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    brief = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=Join()
    )


class QuanbenBookChapterItem(Item):
    book_name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    book_category = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    book_author_name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    chapter_num = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    chapter_name = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )
    content = Field(
        input_processor=MapCompose(str, str.strip),
        output_processor=TakeFirst()
    )