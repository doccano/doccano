import abc
from typing import Dict

from pydantic import BaseModel, validator


class BaseData(BaseModel, abc.ABC):
    filename: str
    meta: Dict = {}

    @classmethod
    def parse(cls, **kwargs):
        return cls.parse_obj(kwargs)

    def __hash__(self):
        return hash(tuple(self.dict()))


class TextData(BaseData):
    text: str

    @validator('text')
    def text_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError('is not empty.')


class FileData(BaseData):
    pass
