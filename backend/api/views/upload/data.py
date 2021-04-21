import abc
from typing import Dict

from pydantic import BaseModel


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


class FileData(BaseData):
    pass
