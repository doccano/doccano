import itertools
from collections import defaultdict
from typing import Any, Dict, List, Type

from .cleaners import Cleaner
from .data import BaseData
from .exceptions import FileParseException
from .labels import Label
from examples.models import Example
from label_types.models import CategoryType, LabelType, SpanType
from labels.models import Label as LabelModel
from projects.models import Project


def group_by_class(instances):
    groups = defaultdict(list)
    for instance in instances:
        groups[instance.__class__].append(instance)
    return groups


class Record:
    """Record represents a data."""

    def __init__(
        self, data: BaseData, label: List[Label] = None, meta: Dict[Any, Any] = None, line_num: int = -1
    ):
        if label is None:
            label = []
        if meta is None:
            meta = {}
        self._data = data
        self._label = label
        self._meta = meta
        self._line_num = line_num

    def __str__(self):
        return f"{self._data}\t{self._label}"

    def clean(self, cleaner: Cleaner):
        label = cleaner.clean(self._label)
        changed = len(label) != len(self.label)
        self._label = label
        if changed:
            return FileParseException(filename=self._data.filename, line_num=self._line_num, message=cleaner.message)

    @property
    def data(self):
        return self._data

    def create_data(self, project) -> Example:
        return self._data.create(project=project, meta=self._meta)

    def create_label(self, project) -> List[LabelType]:
        labels = [label.create(project) for label in self._label]
        return list(filter(None, labels))

    def create_annotation(self, user, example, mapping):
        return [label.create_annotation(user, example, mapping) for label in self._label]

    @property
    def label(self):
        return [label.dict() for label in self._label if label.has_name() and label.name]


class LabeledExamples:
    def __init__(self, records: List[Record]):
        self.records = records

    def create_data(self, project: Project) -> List[Example]:
        return [record.create_data(project) for record in self.records]

    def create_label_type(self, project: Project) -> Dict[Type[LabelType], List[LabelType]]:
        labels = [record.create_label(project) for record in self.records]
        flatten = list(itertools.chain.from_iterable(labels))
        return group_by_class(flatten)

    def create_label(self, project: Project, user, examples: List[Example]) -> Dict[Type[LabelModel], List[LabelModel]]:
        mapping = {}
        label_types: List[Type[LabelType]] = [CategoryType, SpanType]
        for model in label_types:
            for label in model.objects.filter(project=project):
                mapping[label.text] = label

        annotations = list(
            itertools.chain.from_iterable(
                [data.create_annotation(user, example, mapping) for data, example in zip(self.records, examples)]
            )
        )
        return group_by_class(annotations)
