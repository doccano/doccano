from django.test import TestCase
from model_mommy import mommy

from data_export.models import ExportedExample
from projects.tests.utils import prepare_project


class TestExportedExample(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item)
        self.example2 = mommy.make("ExportedExample", project=self.project.item)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_collaborative(self):
        self.prepare_data(collaborative=True)
        examples = ExportedExample.objects.confirmed(self.project.item)
        self.assertEqual(examples.count(), 1)
        self.assertEqual(examples.first(), self.example1)

    def test_filter_by_confirmed_user(self):
        self.prepare_data(collaborative=False)
        examples = ExportedExample.objects.confirmed(self.project.item, user=self.project.admin)
        self.assertEqual(examples.count(), 1)
        self.assertEqual(examples.first(), self.example1)

    def test_filter_by_unconfirmed_user(self):
        self.prepare_data(collaborative=False)
        examples = ExportedExample.objects.confirmed(self.project.item, user=self.project.annotator)
        self.assertEqual(examples.count(), 0)
