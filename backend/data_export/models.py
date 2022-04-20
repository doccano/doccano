import abc
from typing import Any, Dict, Protocol

from django.db import models

from labels.models import Category


class ExportedLabelManager(models.Manager):
    pass


class ExportedLabel(Protocol):
    objects: models.Manager = ExportedLabelManager()

    @abc.abstractmethod
    def dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Please implement this method in the subclass.")


class ExportedCategory(Category):
    def dict(self) -> Dict[str, Any]:
        return {"category": self.label.text}

    class Meta:
        proxy = True
