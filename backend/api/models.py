import string

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
PROJECT_CHOICES = (
    (DOCUMENT_CLASSIFICATION, 'document classification'),
    (SEQUENCE_LABELING, 'sequence labeling'),
    (SEQ2SEQ, 'sequence to sequence'),
    (SPEECH2TEXT, 'speech to text'),
)


class Project(PolymorphicModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    guideline = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='projects')
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)
    randomize_document_order = models.BooleanField(default=False)
    collaborative_annotation = models.BooleanField(default=False)
    single_class_classification = models.BooleanField(default=False)

    def get_annotation_class(self):
        raise NotImplementedError()

    def __str__(self):
        return self.name


class TextClassificationProject(Project):

    def get_annotation_class(self):
        return DocumentAnnotation


class SequenceLabelingProject(Project):

    def get_annotation_class(self):
        return SequenceAnnotation


class Seq2seqProject(Project):

    def get_annotation_class(self):
        return Seq2seqAnnotation


class Speech2textProject(Project):

    def get_annotation_class(self):
        return Speech2textAnnotation


class Label(models.Model):
    PREFIX_KEYS = (
        ('ctrl', 'ctrl'),
        ('shift', 'shift'),
        ('ctrl shift', 'ctrl shift')
    )
    SUFFIX_KEYS = tuple(
        (c, c) for c in string.digits + string.ascii_lowercase
    )

    text = models.CharField(max_length=100)
    prefix_key = models.CharField(max_length=10, blank=True, null=True, choices=PREFIX_KEYS)
    suffix_key = models.CharField(max_length=1, blank=True, null=True, choices=SUFFIX_KEYS)
    project = models.ForeignKey(Project, related_name='labels', on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#209cee')
    text_color = models.CharField(max_length=7, default='#ffffff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def clean(self):
        # Don't allow shortcut key not to have a suffix key.
        if self.prefix_key and not self.suffix_key:
            raise ValidationError('Shortcut key may not have a suffix key.')

        # each shortcut (prefix key + suffix key) can only be assigned to one label
        if self.suffix_key or self.prefix_key:
            other_labels = self.project.labels.exclude(id=self.id)
            if other_labels.filter(suffix_key=self.suffix_key, prefix_key=self.prefix_key).exists():
                raise ValidationError('A label with this shortcut already exists in the project')

        super().clean()

    class Meta:
        unique_together = (
            ('project', 'text'),
        )


class Document(models.Model):
    text = models.TextField()
    project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE)
    meta = models.JSONField(default=dict)
    filename = models.FilePathField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    annotations_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text[:50]

    @property
    def comment_count(self):
        return Comment.objects.filter(document=self.id).count()


class Comment(models.Model):
    text = models.TextField()
    document = models.ForeignKey(Document, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def username(self):
        return self.user.username

    @property
    def document_text(self):
        return self.document.text

    class Meta:
        ordering = ('-created_at', )


class Tag(models.Model):
    text = models.TextField()
    project = models.ForeignKey(Project, related_name='tags', on_delete=models.CASCADE)

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


class DocumentAnnotation(Annotation):
    document = models.ForeignKey(Document, related_name='doc_annotations', on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('document', 'user', 'label')


class SequenceAnnotation(Annotation):
    document = models.ForeignKey(Document, related_name='seq_annotations', on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    start_offset = models.IntegerField()
    end_offset = models.IntegerField()

    def clean(self):
        if self.start_offset >= self.end_offset:
            raise ValidationError('start_offset is after end_offset')

    class Meta:
        unique_together = ('document', 'user', 'label', 'start_offset', 'end_offset')


class Seq2seqAnnotation(Annotation):
    # Override AnnotationManager for custom functionality
    objects = Seq2seqAnnotationManager()

    document = models.ForeignKey(Document, related_name='seq2seq_annotations', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    class Meta:
        unique_together = ('document', 'user', 'text')


class Speech2textAnnotation(Annotation):
    document = models.ForeignKey(Document, related_name='speech2text_annotations', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ('document', 'user')


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RoleMapping(models.Model):
    user = models.ForeignKey(User, related_name='role_mappings', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='role_mappings', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RoleMappingManager()

    def clean(self):
        other_rolemappings = self.project.role_mappings.exclude(id=self.id)

        if other_rolemappings.filter(user=self.user, project=self.project).exists():
            raise ValidationError('This user is already assigned to a role in this project.')

    class Meta:
        unique_together = ("user", "project")


class AutoLabelingConfig(models.Model):
    model_name = models.CharField(max_length=100)
    model_attrs = models.JSONField(default=dict)
    template = models.TextField(default='')
    label_mapping = models.JSONField(default=dict)
    project = models.ForeignKey(Project, related_name='auto_labeling_config', on_delete=models.CASCADE)
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
            raise ValidationError(f'The specified model name {self.model_name} does not exist.')
        except Exception:
            raise ValidationError('The attributes does not match the model.')
