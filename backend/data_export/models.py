from typing import Any, Dict, Protocol, Tuple

from django.db import models

from labels.models import Category, Span


class ExportedLabelManager(models.Manager):
    pass


class ExportedLabel(Protocol):
    objects: models.Manager = ExportedLabelManager()

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Please implement this method in the subclass.")

    def to_string(self) -> str:
        raise NotImplementedError("Please implement this method in the subclass.")

    def to_tuple(self) -> Tuple:
        raise NotImplementedError("Please implement this method in the subclass.")


class ExportedCategory(Category):
    def to_string(self) -> str:
        return self.label.text

    class Meta:
        proxy = True


class ExportedSpan(Span):
    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label.text,
            "start_offset": self.start_offset,
            "end_offset": self.end_offset,
        }

    def to_tuple(self):
        return self.start_offset, self.end_offset, self.label.text

    class Meta:
        proxy = True
