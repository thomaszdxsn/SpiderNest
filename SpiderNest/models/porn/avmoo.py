from pydantic import BaseModel

__all__ = ('AvmooActress',)


class AvmooActress(BaseModel):
    name_cn: str
    name_en: str
    name_jp: str
    info: dict
    avatar: str