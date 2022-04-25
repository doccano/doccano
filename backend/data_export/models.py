from typing import Any, Dict, Protocol, Tuple

from django.db import models

from examples.models import Example
from labels.models import Category, Relation, Span, TextLabel
from projects.models import Project

DATA = "data"


class ExportedExampleManager(models.Manager):
    def confirmed(self, project: Project, user=None):
        if project.collaborative_annotation:
            return self.filter(project=project).exclude(states=None)
        else:
            assert user is not None
            return self.filter(project=project, states__confirmed_by=user)


class ExportedExample(Example):
    objects = ExportedExampleManager()

    def to_dict(self, is_text_project=True) -> Dict[str, Any]:
        return {"id": self.id, DATA: self.text if is_text_project else self.upload_name, **self.meta}

    class Meta:
        proxy = True


class ExportedLabel(Protocol):
    objects: models.Manager

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


class ExportedRelation(Relation):
    def to_dict(self):
        return {"id": self.id, "from_id": self.from_id.id, "to_id": self.to_id.id, "type": self.type.text}

    class Meta:
        proxy = True


class ExportedText(TextLabel):
    def to_string(self) -> str:
        return self.text

    class Meta:
        proxy = True
