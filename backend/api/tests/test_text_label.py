import abc

from django.test import TestCase
from model_mommy import mommy

from api.models import SEQ2SEQ, TextLabel

from .api.utils import prepare_project


class TestTextLabelAnnotation(abc.ABC, TestCase):
    collaborative = False

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(
            SEQ2SEQ,
            collaborative_annotation=cls.collaborative
        )
        cls.example = mommy.make('Example', project=cls.project.item)
        users = cls.project.users
        cls.user = users[0]
        cls.another_user = users[1]
        cls.text_label = TextLabel(
            example=cls.example,
            user=cls.user,
            text='foo'
        )

    def test_can_annotate_category_to_unannotated_data(self):
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)


class TestNonCollaborativeTextLabelAnnotation(TestTextLabelAnnotation):
    collaborative = False

    def test_cannot_annotate_same_text_to_annotated_data(self):
        mommy.make(
            'TextLabel',
            example=self.example,
            user=self.user,
            text=self.text_label.text
        )
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertFalse(can_annotate)

    def test_can_annotate_different_text_to_annotated_data(self):
        mommy.make('TextLabel', example=self.example, user=self.user)
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)

    def test_allow_another_user_to_annotate_same_text(self):
        mommy.make(
            'TextLabel',
            example=self.example,
            user=self.another_user,
            text=self.text_label.text
        )
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)


class TestCollaborativeTextLabelAnnotation(TestTextLabelAnnotation):
    collaborative = True

    def test_deny_another_user_to_annotate_same_text(self):
        mommy.make(
            'TextLabel',
            example=self.example,
            user=self.another_user,
            text=self.text_label.text
        )
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertFalse(can_annotate)

    def test_allow_another_user_to_annotate_different_text(self):
        mommy.make(
            'TextLabel',
            example=self.example,
            user=self.another_user
        )
        can_annotate = TextLabel.objects.can_annotate(self.text_label, self.project.item)
        self.assertTrue(can_annotate)
