import abc

from django.db import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from labels.models import Category
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestCategoryLabeling(abc.ABC, TestCase):
    exclusive = True
    collaborative = False

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(
            ProjectType.DOCUMENT_CLASSIFICATION,
            single_class_classification=cls.exclusive,
            collaborative_annotation=cls.collaborative,
        )
        cls.example = mommy.make("Example", project=cls.project.item)
        cls.label_type = mommy.make("CategoryType", project=cls.project.item)
        cls.user = cls.project.admin
        cls.another_user = cls.project.approver
        cls.category = Category(example=cls.example, label=cls.label_type, user=cls.user)

    def test_can_annotate_category_to_unannotated_data(self):
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertTrue(can_annotate)


class NonCollaborativeMixin:
    def test_cannot_annotate_same_category_to_annotated_data(self):
        mommy.make("Category", example=self.example, label=self.label_type, user=self.user)
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertFalse(can_annotate)

    def test_allow_another_user_to_annotate_same_category(self):
        mommy.make("Category", example=self.example, label=self.label_type, user=self.another_user)
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertTrue(can_annotate)


class TestExclusiveCategoryLabeling(TestCategoryLabeling, NonCollaborativeMixin):
    exclusive = True
    collaborative = False

    def test_cannot_annotate_different_category_to_annotated_data(self):
        mommy.make("Category", example=self.example, user=self.user)
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertFalse(can_annotate)


class TestNonExclusiveCategoryLabeling(TestCategoryLabeling, NonCollaborativeMixin):
    exclusive = False
    collaborative = False

    def test_can_annotate_different_category_to_annotated_data(self):
        mommy.make("Category", example=self.example, user=self.user)
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertTrue(can_annotate)


class CollaborativeMixin:
    def test_deny_another_user_to_annotate_same_category(self):
        mommy.make("Category", example=self.example, label=self.label_type, user=self.another_user)
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertFalse(can_annotate)


class TestCollaborativeExclusiveCategoryLabeling(TestCategoryLabeling, CollaborativeMixin):
    exclusive = True
    collaborative = True

    def test_deny_another_user_to_annotate_different_category(self):
        mommy.make("Category", example=self.example, user=self.another_user)
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertFalse(can_annotate)


class TestCollaborativeNonExclusiveCategoryLabeling(TestCategoryLabeling, CollaborativeMixin):
    exclusive = False
    collaborative = True

    def test_allow_another_user_to_annotate_different_category(self):
        mommy.make("Category", example=self.example, user=self.another_user)
        can_annotate = Category.objects.can_annotate(self.category, self.project.item)
        self.assertTrue(can_annotate)


class TestCategory(TestCase):
    def test_uniqueness(self):
        a = mommy.make("Category")
        with self.assertRaises(IntegrityError):
            Category(example=a.example, user=a.user, label=a.label).save()
