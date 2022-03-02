import abc

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Manager
from polymorphic.models import PolymorphicModel

from roles.models import Role

DOCUMENT_CLASSIFICATION = "DocumentClassification"
SEQUENCE_LABELING = "SequenceLabeling"
SEQ2SEQ = "Seq2seq"
SPEECH2TEXT = "Speech2text"
IMAGE_CLASSIFICATION = "ImageClassification"
INTENT_DETECTION_AND_SLOT_FILLING = "IntentDetectionAndSlotFilling"
PROJECT_CHOICES = (
    (DOCUMENT_CLASSIFICATION, "document classification"),
    (SEQUENCE_LABELING, "sequence labeling"),
    (SEQ2SEQ, "sequence to sequence"),
    (INTENT_DETECTION_AND_SLOT_FILLING, "intent detection and slot filling"),
    (SPEECH2TEXT, "speech to text"),
    (IMAGE_CLASSIFICATION, "image classification"),
)


class Project(PolymorphicModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    guideline = models.TextField(default="", blank=True)
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

    def add_admin(self):
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        Member.objects.create(
            project=self,
            user=self.created_by,
            role=admin_role,
        )

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
    use_relation = models.BooleanField(default=False)

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


class Tag(models.Model):
    text = models.TextField()
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return self.text


class MemberManager(Manager):
    def can_update(self, project: int, member_id: int, new_role: str) -> bool:
        """The project needs at least 1 admin.

        Args:
            project: The project id.
            member_id: The member id.
            new_role: The new role name.

        Returns:
            Whether the mapping can be updated or not.
        """
        queryset = self.filter(project=project, role__name=settings.ROLE_PROJECT_ADMIN)
        if queryset.count() > 1:
            return True
        else:
            admin = queryset.first()
            # we can change the role except for the only admin.
            return admin.id != member_id or new_role == settings.ROLE_PROJECT_ADMIN

    def has_role(self, project_id: int, user: User, role_name: str):
        return self.filter(project=project_id, user=user, role__name=role_name).exists()


class Member(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="role_mappings")
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="role_mappings")
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MemberManager()

    def clean(self):
        members = self.__class__.objects.exclude(id=self.id)
        if members.filter(user=self.user, project=self.project).exists():
            message = "This user is already assigned to a role in this project."
            raise ValidationError(message)

    @property
    def username(self):
        return self.user.username

    class Meta:
        unique_together = ("user", "project")
