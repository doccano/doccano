import pathlib

from django.test import TestCase

from ..models import (DOCUMENT_CLASSIFICATION, SEQ2SEQ, SEQUENCE_LABELING,
                      Category, Example, Label, Span, TextLabel)
from ..tasks import injest_data
from .api.utils import prepare_project


class TestIngestData(TestCase):
    task = 'Any'
    annotation_class = Category

    def setUp(self):
        self.project = prepare_project(self.task)
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
        self.assertEqual(self.annotation_class.objects.count(), expected_annotation)


class TestIngestClassificationData(TestIngestData):
    task = DOCUMENT_CLASSIFICATION
    annotation_class = Category

    def test_jsonl(self):
        filename = 'text_classification/example.jsonl'
        file_format = 'JSONL'
        kwargs = {'column_label': 'labels'}
        self.assert_count(filename, file_format, kwargs, expected_example=4, expected_label=3, expected_annotation=5)

    def test_csv(self):
        filename = 'text_classification/example.csv'
        file_format = 'CSV'
        self.assert_count(filename, file_format, expected_example=4, expected_label=2, expected_annotation=2)

    def test_fasttext(self):
        filename = 'text_classification/example_fasttext.txt'
        file_format = 'fastText'
        self.assert_count(filename, file_format, expected_example=4, expected_label=5, expected_annotation=5)

    def test_excel(self):
        filename = 'text_classification/example.xlsx'
        file_format = 'Excel'
        self.assert_count(filename, file_format, expected_example=3, expected_label=2, expected_annotation=3)

    def test_json(self):
        filename = 'text_classification/example.json'
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


class TestIngestSequenceLabelingData(TestIngestData):
    task = SEQUENCE_LABELING
    annotation_class = Span

    def test_jsonl(self):
        filename = 'sequence_labeling/example.jsonl'
        file_format = 'JSONL'
        self.assert_count(filename, file_format, expected_example=3, expected_label=3, expected_annotation=4)

    def test_conll(self):
        filename = 'sequence_labeling/example.conll'
        file_format = 'CoNLL'
        self.assert_count(filename, file_format, expected_example=3, expected_label=2, expected_annotation=5)


class TestIngestSeq2seqData(TestIngestData):
    task = SEQ2SEQ
    annotation_class = TextLabel

    def test_jsonl(self):
        filename = 'seq2seq/example.jsonl'
        file_format = 'JSONL'
        self.assert_count(filename, file_format, expected_example=3, expected_label=0, expected_annotation=4)

    def test_json(self):
        filename = 'seq2seq/example.json'
        file_format = 'JSON'
        self.assert_count(filename, file_format, expected_example=3, expected_label=0, expected_annotation=4)

    def test_csv(self):
        filename = 'seq2seq/example.csv'
        file_format = 'CSV'
        self.assert_count(filename, file_format, expected_example=4, expected_label=0, expected_annotation=3)
