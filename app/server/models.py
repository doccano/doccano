import string
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage


class Project(models.Model):
    DOCUMENT_CLASSIFICATION = 'DocumentClassification'
    SEQUENCE_LABELING = 'SequenceLabeling'
    Seq2seq = 'Seq2seq'

    PROJECT_CHOICES = (
        (DOCUMENT_CLASSIFICATION, 'document classification'),
        (SEQUENCE_LABELING, 'sequence labeling'),
        (Seq2seq, 'sequence to sequence'),
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    guideline = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User)
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)

    def is_type_of(self, project_type):
        return project_type == self.project_type

    @property
    def image(self):
        if self.is_type_of(self.DOCUMENT_CLASSIFICATION):
            url = staticfiles_storage.url('images/cat-1045782_640.jpg')
        elif self.is_type_of(self.SEQUENCE_LABELING):
            url = staticfiles_storage.url('images/cat-3449999_640.jpg')
        elif self.is_type_of(self.Seq2seq):
            url = staticfiles_storage.url('images/tiger-768574_640.jpg')

        return url

    def __str__(self):
        return self.name


class Label(models.Model):
    KEY_CHOICES = ((u, c) for u, c in zip(string.ascii_lowercase, string.ascii_lowercase))
    COLOR_CHOICES = ()

    text = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=10, choices=KEY_CHOICES)
    project = models.ForeignKey(Project, related_name='labels', on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#209cee')
    text_color = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return self.text

    class Meta:
        unique_together = (
            ('project', 'text'),
            ('project', 'shortcut')
        )


class Document(models.Model):
    text = models.TextField()
    project = models.ForeignKey(Project, related_name='documents', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:50]


class Annotation(models.Model):
    prob = models.FloatField(default=0.0)
    manual = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    document = models.ForeignKey(Document, related_name='seq2seq_annotations', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ('document', 'user', 'text')


from .serializers import *


# temporary solution
class Factory(object):

    @classmethod
    def get_template(cls, project):
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            template_name = 'annotation/document_classification.html'
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            template_name = 'annotation/sequence_labeling.html'
        elif project.is_type_of(Project.Seq2seq):
            template_name = 'annotation/seq2seq.html'
        else:
            raise ValueError('Template does not exist')

        return template_name

    @classmethod
    def get_documents(cls, project, is_null=True):
        docs = project.documents.all()
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            docs = docs.filter(doc_annotations__isnull=is_null)
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            docs = docs.filter(seq_annotations__isnull=is_null)
        elif project.is_type_of(Project.Seq2seq):
            docs = docs.filter(seq2seq_annotations__isnull=is_null)
        else:
            raise ValueError('Invalid project_type')

        return docs

    @classmethod
    def get_project_serializer(cls, project):
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            return DocumentSerializer
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            return SequenceSerializer
        elif project.is_type_of(Project.Seq2seq):
            return Seq2seqSerializer
        else:
            raise ValueError('Invalid project_type')

    @classmethod
    def get_annotation_serializer(cls, project):
        if project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            return DocumentAnnotationSerializer
        elif project.is_type_of(Project.SEQUENCE_LABELING):
            return SequenceAnnotationSerializer
        elif project.is_type_of(Project.Seq2seq):
            return Seq2seqAnnotationSerializer

    @classmethod
    def get_annotations_by_doc(cls, document):
        if document.project.is_type_of(Project.DOCUMENT_CLASSIFICATION):
            return document.doc_annotations.all()
        elif document.project.is_type_of(Project.SEQUENCE_LABELING):
            return document.seq_annotations.all()
        elif document.project.is_type_of(Project.Seq2seq):
            return document.seq2seq_annotations.all()
