import random
import string
import uuid
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

    
from auto_labeling_pipeline.models import RequestModelFactory
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from polymorphic.models import PolymorphicModel

from .managers import (AnnotationManager, RoleMappingManager,
                       Seq2seqAnnotationManager)

DOCUMENT_CLASSIFICATION = 'DocumentClassification'
SEQUENCE_LABELING = 'SequenceLabeling'
SEQ2SEQ = 'Seq2seq'
SPEECH2TEXT = 'Speech2text'
IMAGE_CLASSIFICATION = 'ImageClassification'
PROJECT_CHOICES = (
    (DOCUMENT_CLASSIFICATION, 'document classification'),
    (SEQUENCE_LABELING, 'sequence labeling'),
    (SEQ2SEQ, 'sequence to sequence'),
    (SPEECH2TEXT, 'speech to text'),
    (IMAGE_CLASSIFICATION, 'image classification')
)


class Project(PolymorphicModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    guideline = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='projects')
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)
    random_order = models.BooleanField(default=False)
    collaborative_annotation = models.BooleanField(default=False)
    single_class_classification = models.BooleanField(default=False)

    def get_annotation_class(self):
        raise NotImplementedError()

    def is_task_of(self, task: Literal['text', 'image', 'speech']):
        raise NotImplementedError()

    def __str__(self):
        return self.name


class TextClassificationProject(Project):

    def get_annotation_class(self):
        return Category

    def is_task_of(self, task: Literal['text', 'image', 'speech']):
        return task == 'text'


class SequenceLabelingProject(Project):
    allow_overlapping = models.BooleanField(default=False)
    grapheme_mode = models.BooleanField(default=False)

    def get_annotation_class(self):
        return Span

    def is_task_of(self, task: Literal['text', 'image', 'speech']):
        return task == 'text'


class Seq2seqProject(Project):

    def get_annotation_class(self):
        return TextLabel

    def is_task_of(self, task: Literal['text', 'image', 'speech']):
        return task == 'text'


class Speech2textProject(Project):

    def get_annotation_class(self):
        return TextLabel

    def is_task_of(self, task: Literal['text', 'image', 'speech']):
        return task == 'speech'


class ImageClassificationProject(Project):

    def get_annotation_class(self):
        return Category

    def is_task_of(self, task: Literal['text', 'image', 'speech']):
        return task == 'image'


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
        related_name='labels'
    )
    background_color = models.CharField(max_length=7, default=generate_random_hex_color)
    text_color = models.CharField(max_length=7, default='#ffffff')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def clean(self):
        # Don't allow shortcut key not to have a suffix key.
        if self.prefix_key and not self.suffix_key:
            message = 'Shortcut key may not have a suffix key.'
            raise ValidationError(message)

        # each shortcut (prefix key + suffix key) can only be assigned to one label
        if self.suffix_key or self.prefix_key:
            other_labels = self.project.labels.exclude(id=self.id)
            if other_labels.filter(suffix_key=self.suffix_key, prefix_key=self.prefix_key).exists():
                message = 'A label with the shortcut already exists in the project.'
                raise ValidationError(message)

        super().clean()

    class Meta:
        unique_together = (
            ('project', 'text'),
        )
        ordering = ['created_at']


class Example(models.Model):
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

    class Meta:
        ordering = ['created_at']


class ExampleState(models.Model):
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

    @property
    def confirmed_user_role(self):
        role_mapping = RoleMapping.objects.get(user=self.confirmed_by, project=self.example.project)
        return role_mapping.role


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


class Annotation(models.Model):
    objects = AnnotationManager()

    prob = models.FloatField(default=0.0)
    manual = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Annotation):
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    label = models.ForeignKey(
        to=Label,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (
            'example',
            'user',
            'label'
        )


class Span(Annotation):
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='spans'
    )
    label = models.ForeignKey(
        to=Label,
        on_delete=models.CASCADE
    )
    start_offset = models.IntegerField()
    end_offset = models.IntegerField()

    def validate_unique(self, exclude=None):
        allow_overlapping = getattr(self.example.project, 'allow_overlapping', False)
        is_collaborative = self.example.project.collaborative_annotation
        if allow_overlapping:
            super().validate_unique(exclude=exclude)
            return

        overlapping_span = Span.objects.exclude(id=self.id).filter(example=self.example).filter(
            models.Q(start_offset__gte=self.start_offset, start_offset__lt=self.end_offset) |
            models.Q(end_offset__gt=self.start_offset, end_offset__lte=self.end_offset) |
            models.Q(start_offset__lte=self.start_offset, end_offset__gte=self.end_offset)
        )
        if is_collaborative:
            if overlapping_span.exists():
                raise ValidationError('This overlapping is not allowed in this project.')
        else:
            if overlapping_span.filter(user=self.user).exists():
                raise ValidationError('This overlapping is not allowed in this project.')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_offset__gte=0), name='startOffset >= 0'),
            models.CheckConstraint(check=models.Q(end_offset__gte=0), name='endOffset >= 0'),
            models.CheckConstraint(check=models.Q(start_offset__lt=models.F('end_offset')), name='start < end')
        ]


class TextLabel(Annotation):
    objects = Seq2seqAnnotationManager()
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='texts'
    )
    text = models.TextField()

    class Meta:
        unique_together = (
            'example',
            'user',
            'text'
        )


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RoleMapping(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='role_mappings'
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='role_mappings'
    )
    role = models.ForeignKey(
        to=Role,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RoleMappingManager()

    def clean(self):
        other_rolemappings = self.project.role_mappings.exclude(id=self.id)

        if other_rolemappings.filter(user=self.user, project=self.project).exists():
            message = 'This user is already assigned to a role in this project.'
            raise ValidationError(message)

    class Meta:
        unique_together = ("user", "project")


class AutoLabelingConfig(models.Model):
    model_name = models.CharField(max_length=100)
    model_attrs = models.JSONField(default=dict)
    template = models.TextField(default='')
    label_mapping = models.JSONField(default=dict, blank=True)
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='auto_labeling_config'
    )
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model_name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        try:
            RequestModelFactory.find(self.model_name)
        except NameError:
            message = f'The specified model name {self.model_name} does not exist.'
            raise ValidationError(message)
        except Exception:
            message = 'The attributes does not match the model.'
            raise ValidationError(message)


class RelationTypes(models.Model):
    color = models.TextField()
    name = models.TextField()
    project = models.ForeignKey(Project, related_name='relation_types', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('color', 'name')


class AnnotationRelations(models.Model):
    annotation_id_1 = models.IntegerField()
    annotation_id_2 = models.IntegerField()
    type = models.ForeignKey(RelationTypes, related_name='annotation_relations', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, related_name='annotation_relations', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='annotation_relations', on_delete=models.CASCADE)

    def __str__(self):
        return self.__dict__.__str__()

    class Meta:
        unique_together = ('annotation_id_1', 'annotation_id_2', 'type', 'project')
