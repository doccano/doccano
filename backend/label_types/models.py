import random
import string

from django.core.exceptions import ValidationError
from django.db import models

from projects.models import Project


def generate_random_hex_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


class LabelType(models.Model):
    text = models.CharField(max_length=100, db_index=True)
    prefix_key = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=(("ctrl", "ctrl"), ("shift", "shift"), ("ctrl shift", "ctrl shift")),
    )
    suffix_key = models.CharField(
        max_length=1, blank=True, null=True, choices=tuple((c, c) for c in string.digits + string.ascii_lowercase)
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        # related_name='labels'
    )
    background_color = models.CharField(max_length=7, default=generate_random_hex_color)
    text_color = models.CharField(max_length=7, default="#ffffff")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    @property
    def labels(self):
        raise NotImplementedError()

    def clean(self):
        # Don't allow shortcut key not to have a suffix key.
        if self.prefix_key and not self.suffix_key:
            message = "Shortcut key may not have a suffix key."
            raise ValidationError(message)

        # each shortcut (prefix key + suffix key) can only be assigned to one label
        if self.suffix_key or self.prefix_key:
            other_labels = self.labels.exclude(id=self.id)
            if other_labels.filter(suffix_key=self.suffix_key, prefix_key=self.prefix_key).exists():
                message = "A label with the shortcut already exists in the project."
                raise ValidationError(message)

        super().clean()

    class Meta:
        abstract = True
        constraints = [models.UniqueConstraint(fields=["project", "text"], name="%(app_label)s_%(class)s_is_unique")]
        ordering = ["created_at"]


class CategoryType(LabelType):
    @property
    def labels(self):
        return CategoryType.objects.filter(project=self.project)


class SpanType(LabelType):
    @property
    def labels(self):
        return SpanType.objects.filter(project=self.project)


class RelationType(LabelType):
    @property
    def labels(self):
        return RelationType.objects.filter(project=self.project)
