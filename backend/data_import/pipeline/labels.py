import abc
from itertools import groupby
from typing import Dict, List, Tuple

from .examples import Examples
from .label import Label
from .label_types import LabelTypes
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

    def save(self, user, examples: Examples, **kwargs):
        labels = [
            label.create(user, examples[label.example_uuid], self.types, **kwargs)
            for label in self.labels
            if label.example_uuid in examples
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
    def id_to_span(self) -> Dict[Tuple[int, str], SpanModel]:
        uuids = [str(span.uuid) for span in self.labels]
        spans = SpanModel.objects.filter(uuid__in=uuids)
        uuid_to_span = {span.uuid: span for span in spans}
        return {(span.id, str(span.example_uuid)): uuid_to_span[span.uuid] for span in self.labels}


class Texts(Labels):
    label_model = TextLabelModel


class Relations(Labels):
    label_model = RelationModel

    def save(self, user, examples: Examples, **kwargs):
        id_to_span = kwargs["spans"].id_to_span
        super().save(user, examples, id_to_span=id_to_span)
