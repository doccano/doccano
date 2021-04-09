import abc
from typing import Any, Dict, Union

from pydantic import BaseModel


class Label(BaseModel, abc.ABC):

    @abc.abstractmethod
    def has_name(self) -> bool:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @classmethod
    def parse(cls, obj: Any):
        raise NotImplementedError()

    @abc.abstractmethod
    def replace(self, mapping: Dict[str, int]) -> 'Label':
        raise NotImplementedError

    def __hash__(self):
        return hash(tuple(self.dict()))


class CategoryLabel(Label):
    label: Union[str, int]

    def has_name(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.label

    @classmethod
    def parse(cls, obj: Any):
        if isinstance(obj, str):
            return cls(label=obj)
        raise TypeError(f'{obj} is not str.')

    def replace(self, mapping: Dict[str, int]) -> 'Label':
        label = mapping[self.label]
        return CategoryLabel(label=label)


class OffsetLabel(Label):
    label: Union[str, int]
    start_offset: int
    end_offset: int

    def has_name(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.label

    @classmethod
    def parse(cls, obj: Any):
        if isinstance(obj, list) or isinstance(obj, tuple):
            columns = ['start_offset', 'end_offset', 'label']
            obj = zip(columns, obj)
            return cls.parse_obj(obj)
        elif isinstance(obj, dict):
            return cls.parse_obj(obj)
        else:
            raise TypeError(f'{obj} is invalid type.')

    def replace(self, mapping: Dict[str, int]) -> 'Label':
        label = mapping[self.label]
        return OffsetLabel(
            label=label,
            start_offset=self.start_offset,
            end_offset=self.end_offset
        )


class TextLabel(Label):
    text: str

    def has_name(self) -> bool:
        return False

    @property
    def name(self) -> str:
        return self.text

    @classmethod
    def parse(cls, obj: Any):
        if isinstance(obj, str):
            return cls(text=obj)
        else:
            raise TypeError(f'{obj} is not str.')

    def replace(self, mapping: Dict[str, str]) -> 'Label':
        return self
