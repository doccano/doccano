import abc
import random
import string
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from polymorphic.models import PolymorphicModel

from .managers import ExampleManager, ExampleStateManager

DOCUMENT_CLASSIFICATION = 'DocumentClassification'
SEQUENCE_LABELING = 'SequenceLabeling'
SEQ2SEQ = 'Seq2seq'
SPEECH2TEXT = 'Speech2text'
IMAGE_CLASSIFICATION = 'ImageClassification'
INTENT_DETECTION_AND_SLOT_FILLING = 'IntentDetectionAndSlotFilling'
PROJECT_CHOICES = (
    (DOCUMENT_CLASSIFICATION, 'document classification'),
    (SEQUENCE_LABELING, 'sequence labeling'),
    (SEQ2SEQ, 'sequence to sequence'),
    (INTENT_DETECTION_AND_SLOT_FILLING, 'intent detection and slot filling'),
    (SPEECH2TEXT, 'speech to text'),
    (IMAGE_CLASSIFICATION, 'image classification')
)


class Project(PolymorphicModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    guideline = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)
    random_order = models.BooleanField(default=False)
    collaborative_annotation = models.BooleanField(default=False)
    single_class_classification = models.BooleanField(default=False)

    @property
    @abc.abstractmethod
    def is_text_project(self) -> bool:
        return False

    @property
    def can_define_label(self) -> bool:
        """Whether or not the project can define label(ignoring the type of label)"""
        return False

    @property
    def can_define_relation(self) -> bool:
        """Whether or not the project can define relation."""
        return False

    @property
    def can_define_category(self) -> bool:
        """Whether or not the project can define category."""
        return False

    @property
    def can_define_span(self) -> bool:
        """Whether or not the project can define span."""
        return False

    def __str__(self):
        return self.name


class TextClassificationProject(Project):

    @property
    def is_text_project(self) -> bool:
        return True

    @property
    def can_define_label(self) -> bool:
        return True

    @property
    def can_define_category(self) -> bool:
        return True


class SequenceLabelingProject(Project):
    allow_overlapping = models.BooleanField(default=False)
    grapheme_mode = models.BooleanField(default=False)

    @property
    def is_text_project(self) -> bool:
        return True

    @property
    def can_define_label(self) -> bool:
        return True

    @property
    def can_define_span(self) -> bool:
        return True


class Seq2seqProject(Project):

    @property
    def is_text_project(self) -> bool:
        return True


class IntentDetectionAndSlotFillingProject(Project):

    @property
    def is_text_project(self) -> bool:
        return True

    @property
    def can_define_label(self) -> bool:
        return True

    @property
    def can_define_category(self) -> bool:
        return True

    @property
    def can_define_span(self) -> bool:
        return True


class Speech2textProject(Project):

    @property
    def is_text_project(self) -> bool:
        return False


class ImageClassificationProject(Project):

    @property
    def is_text_project(self) -> bool:
        return False

    @property
    def can_define_label(self) -> bool:
        return True

    @property
    def can_define_category(self) -> bool:
        return True


def generate_random_hex_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'


class Label(models.Model):
    text = models.CharField(max_length=100, db_index=True)
    prefix_key = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=(
            ('ctrl', 'ctrl'),
            ('shift', 'shift'),
            ('ctrl shift', 'ctrl shift')
        )
    )
    suffix_key = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        choices=tuple(
            (c, c) for c in string.digits + string.ascii_lowercase
        )
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        # related_name='labels'
    )
    background_color = models.CharField(max_length=7, default=generate_random_hex_color)
    text_color = models.CharField(max_length=7, default='#ffffff')
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
            message = 'Shortcut key may not have a suffix key.'
            raise ValidationError(message)

        # each shortcut (prefix key + suffix key) can only be assigned to one label
        if self.suffix_key or self.prefix_key:
            other_labels = self.labels.exclude(id=self.id)
            if other_labels.filter(suffix_key=self.suffix_key, prefix_key=self.prefix_key).exists():
                message = 'A label with the shortcut already exists in the project.'
                raise ValidationError(message)

        super().clean()

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'text'],
                name='%(app_label)s_%(class)s_is_unique'
            )
        ]
        ordering = ['created_at']


class CategoryType(Label):

    @property
    def labels(self):
        return CategoryType.objects.filter(project=self.project)


class SpanType(Label):

    @property
    def labels(self):
        return SpanType.objects.filter(project=self.project)


class Example(models.Model):
    objects = ExampleManager()

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    meta = models.JSONField(default=dict)
    filename = models.FileField(default='.', max_length=1024)
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='examples'
    )
    annotations_approved_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def comment_count(self):
        return Comment.objects.filter(example=self.id).count()

    @property
    def data(self):
        if self.project.is_text_project:
            return self.text
        else:
            return str(self.filename)

    class Meta:
        ordering = ['created_at']


class ExampleState(models.Model):
    objects = ExampleStateManager()
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='states'
    )
    confirmed_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    confirmed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('example', 'confirmed_by'),)


class Comment(models.Model):
    text = models.TextField()
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def username(self):
        return self.user.username

    class Meta:
        ordering = ['created_at']


class Tag(models.Model):
    text = models.TextField()
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='tags'
    )

    def __str__(self):
        return self.text


class RelationTypes(models.Model):
    color = models.TextField()
    name = models.TextField()
    project = models.ForeignKey(Project, related_name='relation_types', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('color', 'name')
