from typing import Any, Dict, Protocol, Tuple

from django.db import models

from labels.models import Category


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
