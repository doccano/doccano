from typing import List

from .labels import Label, SpanLabel
from projects.models import Project


class Cleaner:
    def __init__(self, project: Project):
        pass

    def clean(self, labels: List[Label]) -> List[Label]:
        return labels

    @property
    def message(self) -> str:
        return ""


class SpanCleaner(Cleaner):
    def __init__(self, project: Project):
        super().__init__(project)
        self.allow_overlapping = getattr(project, "allow_overlapping", False)

    def clean(self, labels: List[SpanLabel]) -> List[SpanLabel]:  # type: ignore
        if self.allow_overlapping:
            return labels

        labels.sort(key=lambda label: label.start_offset)
        last_offset = -1
        new_labels = []
        for label in labels:
            if label.start_offset >= last_offset:
                last_offset = label.end_offset
                new_labels.append(label)
        return new_labels

    @property
    def message(self) -> str:
        return "This project cannot allow label overlapping. It's cleaned."


class CategoryCleaner(Cleaner):
    def __init__(self, project: Project):
        super().__init__(project)
        self.exclusive = getattr(project, "single_class_classification", False)

    def clean(self, labels: List[Label]) -> List[Label]:
        if self.exclusive:
            return labels[:1]
        else:
            return labels

    @property
    def message(self) -> str:
        return "This project only one label can apply but multiple label found. It's cleaned."
