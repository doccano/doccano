from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework.exceptions import ValidationError
from polymorphic.models import PolymorphicModel
from .utils import get_key_choices


DOCUMENT_CLASSIFICATION = 'DocumentClassification'
SEQUENCE_LABELING = 'SequenceLabeling'
SEQ2SEQ = 'Seq2seq'
PROJECT_CHOICES = (
    (DOCUMENT_CLASSIFICATION, 'document classification'),
    (SEQUENCE_LABELING, 'sequence labeling'),
    (SEQ2SEQ, 'sequence to sequence'),
)


class Project(PolymorphicModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    guideline = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='projects')
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)

    def get_absolute_url(self):
        return reverse('upload', args=[self.id])

    @property
    def image(self):
        raise NotImplementedError()

    def get_template_name(self):
        raise NotImplementedError()

    def get_annotation_serializer(self):
        raise NotImplementedError()

    def get_annotation_class(self):
        raise NotImplementedError()

    def get_file_handler(self, format):
        raise NotImplementedError()

    def __str__(self):
        return self.name


class TextClassificationProject(Project):

    @property
    def image(self):
        return staticfiles_storage.url('images/cats/text_classification.jpg')

    def get_template_name(self):
        return 'annotation/document_classification.html'

    def get_annotation_serializer(self):
        from .serializers import DocumentAnnotationSerializer
        return DocumentAnnotationSerializer

    def get_annotation_class(self):
        return DocumentAnnotation

    def get_file_handler(self, format):
        from .api import PlainTextHandler, CSVClassificationHandler, JsonClassificationHandler
        if format == 'plain':
            return PlainTextHandler(self)
        elif format == 'csv':
            return CSVClassificationHandler(self)
        elif format == 'json':
            return JsonClassificationHandler(self)
        raise ValidationError('format {} is invalid.'.format(format))


class SequenceLabelingProject(Project):

    @property
    def image(self):
        return staticfiles_storage.url('images/cats/sequence_labeling.jpg')

    def get_template_name(self):
        return 'annotation/sequence_labeling.html'

    def get_annotation_serializer(self):
        from .serializers import SequenceAnnotationSerializer
        return SequenceAnnotationSerializer

    def get_annotation_class(self):
        return SequenceAnnotation

    def get_file_handler(self, format):
        from .api import PlainTextHandler, CoNLLHandler, JsonLabelingHandler
        if format == 'plain':
            return PlainTextHandler(self)
        elif format == 'conll':
            return CoNLLHandler(self)
        elif format == 'json':
            return JsonLabelingHandler(self)
        raise ValidationError('format {} is invalid.'.format(format))


class Seq2seqProject(Project):

    @property
    def image(self):
        return staticfiles_storage.url('images/cats/seq2seq.jpg')

    def get_template_name(self):
        return 'annotation/seq2seq.html'

    def get_annotation_serializer(self):
        from .serializers import Seq2seqAnnotationSerializer
        return Seq2seqAnnotationSerializer

    def get_annotation_class(self):
        return Seq2seqAnnotation

    def get_file_handler(self, format):
        from .api import PlainTextHandler, CSVSeq2seqHandler, JsonSeq2seqHandler
        if format == 'plain':
            return PlainTextHandler(self)
        elif format == 'csv':
            return CSVSeq2seqHandler(self)
        elif format == 'json':
            return JsonSeq2seqHandler(self)
        raise ValidationError('format {} is invalid.'.format(format))


class Label(models.Model):
    KEY_CHOICES = get_key_choices()
    COLOR_CHOICES = ()

    text = models.CharField(max_length=100)
    shortcut = models.CharField(max_length=15, blank=True, null=True, choices=KEY_CHOICES)
    project = models.ForeignKey(Project, related_name='labels', on_delete=models.CASCADE)
    background_color = models.CharField(max_length=7, default='#209cee')
    text_color = models.CharField(max_length=7, default='#ffffff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    meta = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]


class Annotation(models.Model):
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
    document = models.ForeignKey(Document, related_name='seq2seq_annotations', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        unique_together = ('document', 'user', 'text')
