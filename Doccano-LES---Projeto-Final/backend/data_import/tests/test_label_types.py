from django.test import TestCase
from model_mommy import mommy

from data_import.pipeline.label_types import LabelTypes
from label_types.models import CategoryType
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestCategoryLabel(TestCase):
    def setUp(self):
        self.project = prepare_project(ProjectType.DOCUMENT_CLASSIFICATION)
        self.user = self.project.admin
        self.example = mommy.make("Example", project=self.project.item)

    def test_create(self):
        label_types = LabelTypes(CategoryType)
        category_types = [CategoryType(text="A", project=self.project.item)]
        label_types.save(category_types)
        self.assertEqual(CategoryType.objects.count(), 1)
        self.assertEqual(CategoryType.objects.first().text, "A")

    def test_update(self):
        label_types = LabelTypes(CategoryType)
        category_types = [CategoryType(text="A", project=self.project.item)]
        label_types.save(category_types)
        label_types.update(self.project.item)
        category_type = label_types["A"]
        self.assertEqual(category_type.text, "A")
