import abc
import uuid
from typing import Dict

from pydantic import BaseModel, validator

from ...models import Example, Project


class BaseData(BaseModel, abc.ABC):
    filename: str
    meta: Dict = {}

    @classmethod
    def parse(cls, **kwargs):
        return cls.parse_obj(kwargs)

    def __hash__(self):
        return hash(tuple(self.dict()))

    @abc.abstractmethod
    def create(self, project: Project) -> Example:
        raise NotImplementedError('Please implement this method in the subclass.')


class TextData(BaseData):
    text: str

    @validator('text')
    def text_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError('is not empty.')

    def create(self, project: Project) -> Example:
        return Example(
            uuid=uuid.uuid4(),
            project=project,
            filename=self.filename,
            text=self.text,
            meta=self.meta
        )


class FileData(BaseData):

    def create(self, project: Project) -> Example:
        return Example(
            uuid=uuid.uuid4(),
            project=project,
            filename=self.filename,
            meta=self.meta
        )
