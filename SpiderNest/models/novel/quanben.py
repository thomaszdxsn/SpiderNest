from pydantic import BaseModel

__all__ = ('QuanbenBookChapter', 'QuanbenBook')


class QuanbenBook(BaseModel):
    name: str
    cover: str
    author_name: str
    status: str
    category: str
    brief: str


class QuanbenBookChapter(BaseModel):
    book_author_name: str
    book_name: str
    book_category: str
    chapter_num: int
    chapter_name: str
    content: str