import abc
from typing import List, Type

from auto_labeling_pipeline.labels import Labels
from django.contrib.auth.models import User

from examples.models import Example
from label_types.models import CategoryType, LabelType, SpanType
from labels.models import Category, Label, Span, TextLabel
from projects.models import Project


class LabelCollection(abc.ABC):
    label_type: Type[LabelType]
    model: Type[Label]

    def __init__(self, labels):
        self.labels = labels

    def transform(self, project: Project, example: Example, user: User) -> List[Label]:
        mapping = {c.text: c for c in self.label_type.objects.filter(project=project)}
        annotations = []
        for label in self.labels:
            if label["label"] not in mapping:
                continue
            label["example"] = example
            label["label"] = mapping[label["label"]]
            label["user"] = user
            annotations.append(self.model(**label))
        return annotations

    def save(self, project: Project, example: Example, user: User):
        labels = self.transform(project, example, user)
        labels = self.model.objects.filter_annotatable_labels(labels, project)
        self.model.objects.bulk_create(labels)


class Categories(LabelCollection):
    label_type = CategoryType
    model = Category


class Spans(LabelCollection):
    label_type = SpanType
    model = Span


class Texts(LabelCollection):
    model = TextLabel

    def transform(self, project: Project, example: Example, user: User) -> List[Label]:
        annotations = []
        for label in self.labels:
            label["example"] = example
            label["user"] = user
            annotations.append(self.model(**label))
        return annotations


def create_labels(task_type: str, labels: Labels) -> LabelCollection:
    return {"Category": Categories, "Span": Spans, "Text": Texts}[task_type](labels.dict())
