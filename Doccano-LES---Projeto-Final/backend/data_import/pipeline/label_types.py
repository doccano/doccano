from typing import Dict, List, Type

from label_types.models import LabelType
from projects.models import Project


class LabelTypes:
    def __init__(self, label_type_class: Type[LabelType]):
        self.types: Dict[str, LabelType] = {}
        self.label_type_class = label_type_class

    def __contains__(self, text: str) -> bool:
        return text in self.types

    def __getitem__(self, text: str) -> LabelType:
        return self.types[text]

    def save(self, label_types: List[LabelType]):
        self.label_type_class.objects.bulk_create(label_types, ignore_conflicts=True)

    def update(self, project: Project):
        types = self.label_type_class.objects.filter(project=project)
        self.types = {label_type.text: label_type for label_type in types}
