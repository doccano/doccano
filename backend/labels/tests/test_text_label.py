import abc

from django.db import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from labels.models import TextLabel
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestTextLabeling(abc.ABC, TestCase):
    collaborative = False

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(ProjectType.SEQ2SEQ, collaborative_annotation=cls.collaborative)
        cls.example = mommy.make("Example", project=cls.project.item)
        cls.user = cls.project.admin
        cls.another_user = cls.project.approver
        cls.text_label = TextLabel(example=cls.example, user=cls.user, text="foo")

    def test_can_annotate_category_to_unannotated_data(self):
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)

    def test_uniqueness(self):
        a = mommy.make("TextLabel")
        with self.assertRaises(IntegrityError):
            TextLabel(example=a.example, user=a.user, text=a.text).save()


class TestNonCollaborativeTextLabeling(TestTextLabeling):
    collaborative = False

    def test_cannot_annotate_same_text_to_annotated_data(self):
        mommy.make("TextLabel", example=self.example, user=self.user, text=self.text_label.text)
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertFalse(can_annotate)

    def test_can_annotate_different_text_to_annotated_data(self):
        mommy.make("TextLabel", example=self.example, user=self.user)
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)

    def test_allow_another_user_to_annotate_same_text(self):
        mommy.make("TextLabel", example=self.example, user=self.another_user, text=self.text_label.text)
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)


class TestCollaborativeTextLabeling(TestTextLabeling):
    collaborative = True

    def test_deny_another_user_to_annotate_same_text(self):
        mommy.make("TextLabel", example=self.example, user=self.another_user, text=self.text_label.text)
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertFalse(can_annotate)

    def test_allow_another_user_to_annotate_different_text(self):
        mommy.make("TextLabel", example=self.example, user=self.another_user)
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)
