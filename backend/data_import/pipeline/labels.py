import abc
from itertools import groupby
from typing import Dict, List

from pydantic import UUID4

from .label import Label
from .label_types import LabelTypes
from examples.models import Example
from labels.models import Category as CategoryModel
from labels.models import Label as LabelModel
from labels.models import Relation as RelationModel
from labels.models import Span as SpanModel
from labels.models import TextLabel as TextLabelModel
from projects.models import Project


class Labels(abc.ABC):
    label_model = LabelModel

    def __init__(self, labels: List[Label], types: LabelTypes):
        self.labels = labels
        self.types = types

    def __len__(self) -> int:
        return len(self.labels)

    def clean(self, project: Project):
        pass

    def save_types(self, project: Project):
        types = [label.create_type(project) for label in self.labels]
        filtered_types = list(filter(None, types))
        self.types.save(filtered_types)
        self.types.update(project)

    @property
    def uuid_to_example(self) -> Dict[UUID4, Example]:
        example_uuids = {str(label.example_uuid) for label in self.labels}
        examples = Example.objects.filter(uuid__in=example_uuids)
        return {example.uuid: example for example in examples}

    def save(self, user, **kwargs):
        uuid_to_example = self.uuid_to_example
        labels = [
            label.create(user, uuid_to_example[label.example_uuid], self.types, **kwargs)
            for label in self.labels
            if label.example_uuid in uuid_to_example
        ]
        self.label_model.objects.bulk_create(labels)


class Categories(Labels):
    label_model = CategoryModel

    def clean(self, project: Project):
        exclusive = getattr(project, "single_class_classification", False)
        if exclusive:
            groups = groupby(self.labels, lambda label: label.example_uuid)
            self.labels = [next(group) for _, group in groups]


class Spans(Labels):
    label_model = SpanModel

    def clean(self, project: Project):
        allow_overlapping = getattr(project, "allow_overlapping", False)
        if allow_overlapping:
            return
        spans = []
        groups = groupby(self.labels, lambda label: label.example_uuid)
        for _, group in groups:
            labels = sorted(group)
            last_offset = -1
            for label in labels:
                if getattr(label, "start_offset") >= last_offset:
                    last_offset = getattr(label, "end_offset")
                    spans.append(label)
        self.labels = spans

    @property
    def id_to_span(self) -> Dict[int, SpanModel]:
        span_uuids = [str(label.uuid) for label in self.labels]
        spans = SpanModel.objects.filter(uuid__in=span_uuids)
        uuid_to_span = {span.uuid: span for span in spans}
        return {span.id: uuid_to_span[span.uuid] for span in self.labels}


class Texts(Labels):
    label_model = TextLabelModel


class Relations(Labels):
    label_model = RelationModel

    def save(self, user, **kwargs):
        id_to_span = kwargs["spans"].id_to_span
        super().save(user, id_to_span=id_to_span)
