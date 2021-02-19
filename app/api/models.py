import string

from auto_labeling_pipeline.models import RequestModelFactory
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from polymorphic.models import PolymorphicModel

from .managers import AnnotationManager, Seq2seqAnnotationManager

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
    guideline = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='projects')
    project_type = models.CharField(max_length=30, choices=PROJECT_CHOICES)
    randomize_document_order = models.BooleanField(default=False)
    collaborative_annotation = models.BooleanField(default=False)
    single_class_classification = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('upload', args=[self.id])

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


class Speech2textProject(Project):

    def get_bundle_name(self):
        return 'speech2text'

    def get_bundle_name_upload(self):
        return 'upload_speech2text'

    def get_bundle_name_download(self):
        return 'download_speech2text'

    def get_annotation_serializer(self):
        from .serializers import Speech2textAnnotationSerializer
        return Speech2textAnnotationSerializer

    def get_annotation_class(self):
        return Speech2textAnnotation

    def get_storage(self, data):
        from .utils import Speech2textStorage
        return Speech2textStorage(data, self)


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
    meta = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    annotations_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    text = models.TextField()
    document = models.ForeignKey(Document, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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

    def clean(self):
        other_rolemappings = self.project.role_mappings.exclude(id=self.id)

        if other_rolemappings.filter(user=self.user, project=self.project).exists():
            raise ValidationError('This user is already assigned to a role in this project.')

    class Meta:
        unique_together = ("user", "project", "role")


@receiver(post_save, sender=RoleMapping)
def add_linked_project(sender, instance, created, **kwargs):
    if not created:
        return
    userInstance = instance.user
    projectInstance = instance.project
    if userInstance and projectInstance:
        user = User.objects.get(pk=userInstance.pk)
        project = Project.objects.get(pk=projectInstance.pk)
        user.projects.add(project)
        user.save()


@receiver(post_save)
def add_superusers_to_project(sender, instance, created, **kwargs):
    if not created:
        return
    if sender not in Project.__subclasses__():
        return
    superusers = User.objects.filter(is_superuser=True)
    admin_role = Role.objects.filter(name=settings.ROLE_PROJECT_ADMIN).first()
    if superusers and admin_role:
        RoleMapping.objects.bulk_create(
            [RoleMapping(role_id=admin_role.id, user_id=superuser.id, project_id=instance.id)
             for superuser in superusers]
        )


@receiver(post_save, sender=User)
def add_new_superuser_to_projects(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        admin_role = Role.objects.filter(name=settings.ROLE_PROJECT_ADMIN).first()
        projects = Project.objects.all()
        if admin_role and projects:
            RoleMapping.objects.bulk_create(
                [RoleMapping(role_id=admin_role.id, user_id=instance.id, project_id=project.id)
                 for project in projects]
            )


@receiver(pre_delete, sender=RoleMapping)
def delete_linked_project(sender, instance, using, **kwargs):
    userInstance = instance.user
    projectInstance = instance.project
    if userInstance and projectInstance:
        user = User.objects.get(pk=userInstance.pk)
        project = Project.objects.get(pk=projectInstance.pk)
        user.projects.remove(project)
        user.save()


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
