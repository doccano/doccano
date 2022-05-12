import itertools
from collections import defaultdict
from typing import Any, Dict, List, Optional, Type

from .cleaners import Cleaner
from .data import BaseData
from .exceptions import FileParseException
from .labels import Label, RelationLabel, SpanLabel
from examples.models import Example
from label_types.models import CategoryType, LabelType, RelationType, SpanType
from labels.models import Label as LabelModel
from labels.models import Relation, Span
from projects.models import Project


def group_by_class(instances):
    groups = defaultdict(list)
    for instance in instances:
        groups[instance.__class__].append(instance)
    return groups


class Record:
    """Record represents a data."""

    def __init__(self, data: BaseData, label: List[Label] = None, meta: Dict[Any, Any] = None, line_num: int = -1):
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

    def create_label_type(self, project) -> List[LabelType]:
        labels = [label.create_type(project) for label in self._label]
        return list(filter(None, labels))

    def create_label(
        self, user, example, mapping, label_class: Optional[Type[Label]] = None, **kwargs
    ) -> List[LabelModel]:
        if label_class is None:
            return [label.create(user, example, mapping) for label in self._label]
        else:
            return [
                label.create(user, example, mapping, **kwargs)
                for label in self._label
                if isinstance(label, label_class)
            ]

    def select_label(self, label_class: Type[Label]) -> List[Label]:
        return [label for label in self._label if isinstance(label, label_class)]

    @property
    def label(self):
        return [label.dict() for label in self._label if label.has_name() and label.name]


class LabeledExamples:
    def __init__(self, records: List[Record]):
        self.records = records

    def create_data(self, project: Project) -> List[Example]:
        examples = [record.create_data(project) for record in self.records]
        examples = Example.objects.bulk_create(examples)
        return examples

    def create_label_type(self, project: Project):
        labels = [record.create_label_type(project) for record in self.records]
        flatten = itertools.chain.from_iterable(labels)
        for label_type_class, instances in group_by_class(flatten).items():
            label_type_class.objects.bulk_create(instances, ignore_conflicts=True)

    def create_label(self, project: Project, user, examples: List[Example]):
        mapping = {}
        label_types: List[Type[LabelType]] = [CategoryType, SpanType]
        for model in label_types:
            for label in model.objects.filter(project=project):
                mapping[label.text] = label

        labels = itertools.chain.from_iterable(
            [data.create_label(user, example, mapping) for data, example in zip(self.records, examples)]
        )
        for label_class, instances in group_by_class(labels).items():
            label_class.objects.bulk_create(instances)


class RelationExamples(LabeledExamples):
    def create_label(self, project: Project, user, examples: List[Example]):
        mapping = {}
        label_types: List[Type[LabelType]] = [RelationType, SpanType]
        for model in label_types:
            for label in model.objects.filter(project=project):
                mapping[label.text] = label

        labels = list(
            itertools.chain.from_iterable(
                [data.create_label(user, example, mapping, SpanLabel) for data, example in zip(self.records, examples)]
            )
        )
        uuids = [label.uuid for label in labels]
        Span.objects.bulk_create(labels)
        # filter spans by uuid
        original_spans = list(
            itertools.chain.from_iterable(example.select_label(SpanLabel) for example in self.records)
        )
        uuid_to_span = {span.uuid: span for span in Span.objects.filter(uuid__in=uuids)}
        # create mapping from id to span
        # this is needed to create the relation
        span_mapping = {span.id: uuid_to_span[span.uuid] for span in original_spans}
        # then, replace from_id and to_id with the span id
        relations = itertools.chain.from_iterable(
            [
                data.create_label(user, example, mapping, RelationLabel, span_mapping=span_mapping)
                for data, example in zip(self.records, examples)
            ]
        )
        Relation.objects.bulk_create(relations)
