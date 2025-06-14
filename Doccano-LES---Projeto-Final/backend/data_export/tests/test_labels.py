from django.test import TestCase
from model_mommy import mommy

from ..pipeline.labels import Categories
from data_export.models import ExportedExample
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestLabels(TestCase):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.example1 = mommy.make("ExportedExample", project=self.project.item)
        self.example2 = mommy.make("ExportedExample", project=self.project.item)
        self.category1 = mommy.make("ExportedCategory", example=self.example1, user=self.project.admin)
        self.examples = ExportedExample.objects.all()

    def test_find_by(self):
        categories = Categories(self.examples)
        result = categories.find_by(self.example1.id)
        self.assertEqual(len(result[Categories.column]), 1)
        result = categories.find_by(self.example2.id)
        self.assertEqual(len(result[Categories.column]), 0)

    def test_find_by_with_user(self):
        categories = Categories(self.examples, user=self.project.annotator)
        result = categories.find_by(self.example1.id)
        self.assertEqual(len(result[Categories.column]), 0)
