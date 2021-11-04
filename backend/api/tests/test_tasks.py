import pathlib

from django.test import TestCase

from ..models import Category, Example, Label
from ..tasks import injest_data
from .api.utils import prepare_project


class TestIngestClassificationData(TestCase):

    def setUp(self):
        self.project = prepare_project(task='DocumentClassification')
        self.user = self.project.users[0]
        self.data_path = pathlib.Path(__file__).parent / 'data'

    def assert_count(self,
                     filename,
                     file_format,
                     kwargs=None,
                     expected_example=0,
                     expected_label=0,
                     expected_annotation=0):
        filenames = [str(self.data_path / filename)]
        kwargs = kwargs or {}
        injest_data(self.user.id, self.project.item.id, filenames, file_format, **kwargs)
        self.assertEqual(Example.objects.count(), expected_example)
        self.assertEqual(Label.objects.count(), expected_label)
        self.assertEqual(Category.objects.count(), expected_annotation)

    def test_jsonl(self):
        filename = 'classification.jsonl'
        file_format = 'JSONL'
        kwargs = {'column_label': 'labels'}
        self.assert_count(filename, file_format, kwargs, expected_example=4, expected_label=3, expected_annotation=5)

    def test_csv(self):
        filename = 'example.csv'
        file_format = 'CSV'
        self.assert_count(filename, file_format, expected_example=4, expected_label=2, expected_annotation=2)

    def test_fasttext(self):
        filename = 'example_fasttext.txt'
        file_format = 'fastText'
        self.assert_count(filename, file_format, expected_example=4, expected_label=5, expected_annotation=5)

    def test_excel(self):
        filename = 'example.xlsx'
        file_format = 'Excel'
        self.assert_count(filename, file_format, expected_example=3, expected_label=2, expected_annotation=3)

    def test_json(self):
        filename = 'example.json'
        file_format = 'JSON'
        self.assert_count(filename, file_format, expected_example=4, expected_label=3, expected_annotation=5)

    def test_textfile(self):
        filename = 'example.txt'
        file_format = 'TextFile'
        self.assert_count(filename, file_format, expected_example=1, expected_label=0, expected_annotation=0)

    def test_textline(self):
        filename = 'example.txt'
        file_format = 'TextLine'
        self.assert_count(filename, file_format, expected_example=3, expected_label=0, expected_annotation=0)
