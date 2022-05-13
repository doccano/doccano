import abc
import uuid
from typing import Any, Dict, Optional

import pydantic.error_wrappers
from pydantic import UUID4, BaseModel, validator

from label_types.models import CategoryType, LabelType, RelationType, SpanType
from labels.models import Category
from labels.models import Label as LabelModel
from labels.models import Relation, Span
from labels.models import TextLabel as TL
from projects.models import Project


class Label(BaseModel, abc.ABC):
    id: int = -1
    uuid: UUID4

    def __init__(self, **data):
        data["uuid"] = uuid.uuid4()
        super().__init__(**data)

    @classmethod
    def parse(cls, obj: Any):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_type(self, project: Project) -> Optional[LabelType]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, user, example, mapping, **kwargs) -> LabelModel:
        raise NotImplementedError

    def __hash__(self):
        return hash(tuple(self.dict()))


class CategoryLabel(Label):
    label: str

    @validator("label")
    def label_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError("is not empty.")

    @classmethod
    def parse(cls, obj: Any):
        try:
            return cls(label=obj)
        except pydantic.error_wrappers.ValidationError:
            return None

    def create_type(self, project: Project) -> Optional[LabelType]:
        return CategoryType(text=self.label, project=project)

    def create(self, user, example, mapping: Dict[str, LabelType], **kwargs):
        return Category(uuid=self.uuid, user=user, example=example, label=mapping[self.label])


class SpanLabel(Label):
    label: str
    start_offset: int
    end_offset: int

    @classmethod
    def parse(cls, obj: Any):
        try:
            if isinstance(obj, list) or isinstance(obj, tuple):
                columns = ["start_offset", "end_offset", "label"]
                obj = zip(columns, obj)
                return cls.parse_obj(obj)
            elif isinstance(obj, dict):
                return cls.parse_obj(obj)
        except pydantic.error_wrappers.ValidationError:
            return None

    def create_type(self, project: Project) -> Optional[LabelType]:
        return SpanType(text=self.label, project=project)

    def create(self, user, example, mapping: Dict[str, LabelType], **kwargs):
        return Span(
            uuid=self.uuid,
            user=user,
            example=example,
            start_offset=self.start_offset,
            end_offset=self.end_offset,
            label=mapping[self.label],
        )


class TextLabel(Label):
    text: str

    @classmethod
    def parse(cls, obj: Any):
        try:
            return cls(text=obj)
        except pydantic.error_wrappers.ValidationError:
            return None

    def create_type(self, project: Project) -> Optional[LabelType]:
        return None

    def create(self, user, example, mapping, **kwargs):
        return TL(uuid=self.uuid, user=user, example=example, text=self.text)


class RelationLabel(Label):
    from_id: int
    to_id: int
    type: str

    @classmethod
    def parse(cls, obj: Any):
        try:
            return cls.parse_obj(obj)
        except pydantic.error_wrappers.ValidationError:
            return None

    def create_type(self, project: Project) -> Optional[LabelType]:
        return RelationType(text=self.type, project=project)

    def create(self, user, example, mapping: Dict[str, LabelType], **kwargs):
        return Relation(
            uuid=self.uuid,
            user=user,
            example=example,
            type=mapping[self.type],
            from_id=kwargs["span_mapping"][self.from_id],
            to_id=kwargs["span_mapping"][self.to_id],
        )
