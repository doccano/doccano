import abc
from itertools import groupby
from typing import Dict, List

from pydantic import UUID4

from .label import Label
from .label_types import LabelTypes
from examples.models import Example
from labels.models import Category as CategoryModel
from labels.models import Relation as RelationModel
from labels.models import Span as SpanModel
from labels.models import TextLabel as TextLabelModel
from projects.models import Project


class Labels(abc.ABC):
    def __init__(self, labels: List[Label], types: LabelTypes):
        self.labels = labels
        self.types = types

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

    @abc.abstractmethod
    def save(self, user, **kwargs):
        raise NotImplementedError()


class Categories(Labels):
    def clean(self, project: Project):
        exclusive = getattr(project, "single_class_classification", False)
        if exclusive:
            groups = groupby(self.labels, lambda label: label.example_uuid)
            self.labels = [next(group) for _, group in groups]

    def save(self, user, **kwargs):
        uuid_to_example = self.uuid_to_example
        categories = [
            category.create(user, uuid_to_example[category.example_uuid], self.types) for category in self.labels
        ]
        CategoryModel.objects.bulk_create(categories)


class Spans(Labels):
    def clean(self, project: Project):
        allow_overlapping = getattr(project, "allow_overlapping", False)
        if allow_overlapping:
            return
        self.labels.sort()
        last_offset = -1
        spans = []
        for label in self.labels:
            if getattr(label, "start_offset") >= last_offset:
                last_offset = getattr(label, "end_offset")
                spans.append(label)
        self.labels = spans

    def save(self, user, **kwargs):
        uuid_to_example = self.uuid_to_example
        spans = [span.create(user, uuid_to_example[span.example_uuid], self.types) for span in self.labels]
        SpanModel.objects.bulk_create(spans)

    @property
    def id_to_span(self) -> Dict[int, SpanModel]:
        span_uuids = [str(label.uuid) for label in self.labels]
        spans = SpanModel.objects.filter(uuid__in=span_uuids)
        uuid_to_span = {span.uuid: span for span in spans}
        return {span.id: uuid_to_span[span.uuid] for span in self.labels}


class Texts(Labels):
    def save(self, user, **kwargs):
        uuid_to_example = self.uuid_to_example
        texts = [text.create(user, uuid_to_example[text.example_uuid], self.types) for text in self.labels]
        TextLabelModel.objects.bulk_create(texts)


class Relations(Labels):
    def save(self, user, **kwargs):
        id_to_span = kwargs["spans"].id_to_span
        uuid_to_example = self.uuid_to_example
        relations = [
            relation.create(user, uuid_to_example[relation.example_uuid], self.types, id_to_span=id_to_span)
            for relation in self.labels
        ]
        RelationModel.objects.bulk_create(relations)
