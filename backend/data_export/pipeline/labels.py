"""
Represents label collection.
"""
import abc
from collections import defaultdict
from typing import Dict, List, Tuple

from django.db.models import QuerySet

from data_export.models import (
    ExportedBoundingBox,
    ExportedCategory,
    ExportedExample,
    ExportedLabel,
    ExportedRelation,
    ExportedSegmentation,
    ExportedSpan,
    ExportedText,
)


class Labels(abc.ABC):
    label_class = ExportedLabel
    column = "labels"
    fields: Tuple[str, ...] = ("example", "label")  # To boost performance

    def __init__(self, examples: QuerySet[ExportedExample], user=None):
        self.label_groups = defaultdict(list)
        labels = self.label_class.objects.filter(example__in=examples)
        if user:
            labels = labels.filter(user=user)
        for label in labels.select_related(*self.fields):
            self.label_groups[label.example.id].append(label)

    def find_by(self, example_id: int) -> Dict[str, List[ExportedLabel]]:
        return {self.column: self.label_groups[example_id]}


class Categories(Labels):
    label_class = ExportedCategory
    column = "categories"
    fields = ("example", "label")


class Spans(Labels):
    label_class = ExportedSpan
    column = "entities"
    fields = ("example", "label")


class Relations(Labels):
    label_class = ExportedRelation
    column = "relations"
    fields = ("example", "type")


class Texts(Labels):
    label_class = ExportedText
    column = "labels"
    fields = ("example",)


class BoundingBoxes(Labels):
    label_class = ExportedBoundingBox
    column = "labels"
    fields = ("example", "label")


class Segments(Labels):
    label_class = ExportedSegmentation
    column = "labels"
    fields = ("example", "label")
