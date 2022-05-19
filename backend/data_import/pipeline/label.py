import abc
import uuid
from typing import Any, Optional

from pydantic import UUID4, BaseModel, validator

from .label_types import LabelTypes
from examples.models import Example
from label_types.models import CategoryType, LabelType, RelationType, SpanType
from labels.models import Category as CategoryModel
from labels.models import Label as LabelModel
from labels.models import Relation as RelationModel
from labels.models import Span as SpanModel
from labels.models import TextLabel as TextLabelModel
from projects.models import Project


class Label(BaseModel, abc.ABC):
    id: int = -1
    uuid: UUID4
    example_uuid: UUID4

    def __init__(self, **data):
        data["uuid"] = uuid.uuid4()
        super().__init__(**data)

    @abc.abstractmethod
    def __lt__(self, other):
        raise NotImplementedError()

    @classmethod
    def parse(cls, example_uuid: UUID4, obj: Any):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_type(self, project: Project) -> Optional[LabelType]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, user, example: Example, types: LabelTypes, **kwargs) -> LabelModel:
        raise NotImplementedError

    def __hash__(self):
        return hash(tuple(self.dict()))


class CategoryLabel(Label):
    label: str

    def __lt__(self, other):
        return self.label < other.label

    @validator("label")
    def label_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError("is not empty.")

    @classmethod
    def parse(cls, example_uuid: UUID4, obj: Any):
        return cls(example_uuid=example_uuid, label=obj)

    def create_type(self, project: Project) -> Optional[LabelType]:
        return CategoryType(text=self.label, project=project)

    def create(self, user, example: Example, types: LabelTypes, **kwargs):
        return CategoryModel(uuid=self.uuid, user=user, example=example, label=types.get_by_text(self.label))


class SpanLabel(Label):
    label: str
    start_offset: int
    end_offset: int

    def __lt__(self, other):
        return self.start_offset < other.start_offset

    @classmethod
    def parse(cls, example_uuid: UUID4, obj: Any):
        if isinstance(obj, list) or isinstance(obj, tuple):
            columns = ["start_offset", "end_offset", "label"]
            obj = zip(columns, obj)
            return cls(example_uuid=example_uuid, **dict(obj))
        elif isinstance(obj, dict):
            return cls(example_uuid=example_uuid, **obj)
        raise ValueError("SpanLabel.parse()")

    def create_type(self, project: Project) -> Optional[LabelType]:
        return SpanType(text=self.label, project=project)

    def create(self, user, example: Example, types: LabelTypes, **kwargs):
        return SpanModel(
            uuid=self.uuid,
            user=user,
            example=example,
            start_offset=self.start_offset,
            end_offset=self.end_offset,
            label=types.get_by_text(self.label),
        )


class TextLabel(Label):
    text: str

    def __lt__(self, other):
        return self.text < other.text

    @validator("text")
    def text_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError("is not empty.")

    @classmethod
    def parse(cls, example_uuid: UUID4, obj: Any):
        return cls(example_uuid=example_uuid, text=obj)

    def create_type(self, project: Project) -> Optional[LabelType]:
        return None

    def create(self, user, example: Example, types: LabelTypes, **kwargs):
        return TextLabelModel(uuid=self.uuid, user=user, example=example, text=self.text)


class RelationLabel(Label):
    from_id: int
    to_id: int
    type: str

    def __lt__(self, other):
        return self.from_id < other.from_id

    @classmethod
    def parse(cls, example_uuid: UUID4, obj: Any):
        return cls(example_uuid=example_uuid, **obj)

    def create_type(self, project: Project) -> Optional[LabelType]:
        return RelationType(text=self.type, project=project)

    def create(self, user, example: Example, types: LabelTypes, **kwargs):
        return RelationModel(
            uuid=self.uuid,
            user=user,
            example=example,
            type=types.get_by_text(self.type),
            from_id=kwargs["id_to_span"][self.from_id],
            to_id=kwargs["id_to_span"][self.to_id],
        )
