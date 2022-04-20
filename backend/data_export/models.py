import abc
from typing import Any, Dict, Protocol

from labels.models import Category


class ExportedLabel(Protocol):
    @abc.abstractmethod
    def dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Please implement this method in the subclass.")


class ExportedCategory(Category):
    def dict(self) -> Dict[str, Any]:
        return {"category": self.label.text}

    class Meta:
        proxy = True
