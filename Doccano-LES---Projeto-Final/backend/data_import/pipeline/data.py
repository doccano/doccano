import abc
from typing import Any, Dict

from pydantic import UUID4, BaseModel, validator

from examples.models import Example
from projects.models import Project


class BaseData(BaseModel, abc.ABC):
    filename: str
    upload_name: str
    uuid: UUID4
    meta: Dict[Any, Any] = {}

    def __init__(self, **data):
        super().__init__(**data)

    @classmethod
    def parse(cls, example_uuid: UUID4, filename: str, upload_name: str, text: str = "", **kwargs):
        return cls(uuid=example_uuid, filename=filename, upload_name=upload_name, text=text, meta=kwargs)

    def __hash__(self):
        return hash(tuple(self.dict()))

    @abc.abstractmethod
    def create(self, project: Project) -> Example:
        raise NotImplementedError("Please implement this method in the subclass.")


class TextData(BaseData):
    text: str

    @validator("text")
    def text_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError("The empty text is not allowed.")

    def create(self, project: Project) -> Example:
        return Example(
            uuid=self.uuid,
            project=project,
            filename=self.filename,
            upload_name=self.upload_name,
            text=self.text,
            meta=self.meta,
        )


class BinaryData(BaseData):
    def create(self, project: Project) -> Example:
        return Example(
            uuid=self.uuid,
            project=project,
            filename=self.filename,
            upload_name=self.upload_name,
            text=None,
            meta=self.meta,
        )
