import string

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel

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
    randomize_document_order = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('upload', args=[self.id])

    @property
    def image(self):
        raise NotImplementedError()

    def get_bundle_name(self):
        raise NotImplementedError()

    def get_bundle_name_upload(self):
        raise NotImplementedError()

    def get_bundle_name_download(self):
        raise NotImplementedError()

    def get_annotation_serializer(self):
        raise NotImplementedError()

    def get_annotation_class(self):
        raise NotImplementedError()

    def get_storage(self, data):
        raise NotImplementedError()

    def __str__(self):
        return self.name


class TextClassificationProject(Project):

    @property
    def image(self):
        return staticfiles_storage.url('assets/images/cats/text_classification.jpg')

    def get_bundle_name(self):
        return 'document_classification'

    def get_bundle_name_upload(self):
        return 'upload_text_classification'

    def get_bundle_name_download(self):
        return 'download_text_classification'

    def get_annotation_serializer(self):
        from .serializers import DocumentAnnotationSerializer
        return DocumentAnnotationSerializer

    def get_annotation_class(self):
        return DocumentAnnotation

    def get_storage(self, data):
        from .utils import ClassificationStorage
        return ClassificationStorage(data, self)


class SequenceLabelingProject(Project):

    @property
    def image(self):
        return staticfiles_storage.url('assets/images/cats/sequence_labeling.jpg')

    def get_bundle_name(self):
        return 'sequence_labeling'

    def get_bundle_name_upload(self):
        return 'upload_sequence_labeling'

    def get_bundle_name_download(self):
        return 'download_sequence_labeling'

    def get_annotation_serializer(self):
        from .serializers import SequenceAnnotationSerializer
        return SequenceAnnotationSerializer

    def get_annotation_class(self):
        return SequenceAnnotation

    def get_storage(self, data):
        from .utils import SequenceLabelingStorage
        return SequenceLabelingStorage(data, self)


class Seq2seqProject(Project):

    @property
    def image(self):
        return staticfiles_storage.url('assets/images/cats/seq2seq.jpg')

    def get_bundle_name(self):
        return 'seq2seq'

    def get_bundle_name_upload(self):
        return 'upload_seq2seq'

    def get_bundle_name_download(self):
        return 'download_seq2seq'

    def get_annotation_serializer(self):
        from .serializers import Seq2seqAnnotationSerializer
        return Seq2seqAnnotationSerializer

    def get_annotation_class(self):
        return Seq2seqAnnotation

    def get_storage(self, data):
        from .utils import Seq2seqStorage
        return Seq2seqStorage(data, self)


class Label(models.Model):
    PREFIX_KEYS = (
        ('ctrl', 'ctrl'),
        ('shift', 'shift'),
        ('ctrl shift', 'ctrl shift')
    )
    SUFFIX_KEYS = tuple(
        (c, c) for c in string.ascii_lowercase
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
        super().clean()

    def validate_unique(self, exclude=None):
        # Don't allow to save same shortcut key when prefix_key is null.
        if Label.objects.exclude(id=self.id).filter(suffix_key=self.suffix_key,
                                                    prefix_key__isnull=True).exists():
            raise ValidationError('Duplicate key.')
        super().validate_unique(exclude)

    class Meta:
        unique_together = (
            ('project', 'text'),
            ('project', 'prefix_key', 'suffix_key')
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
