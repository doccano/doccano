import pathlib

from django.test import TestCase

from data_import.celery_tasks import import_dataset
from examples.models import Example
from label_types.models import CategoryType, SpanType
from labels.models import Category, Span
from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
)
from projects.tests.utils import prepare_project


class TestImportData(TestCase):
    task = "Any"
    annotation_class = Category

    def setUp(self):
        self.project = prepare_project(self.task)
        self.user = self.project.admin
        self.data_path = pathlib.Path(__file__).parent / "data"

    def import_dataset(self, filename, file_format, kwargs=None):
        filenames = [str(self.data_path / filename)]
        kwargs = kwargs or {}
        return import_dataset(self.user.id, self.project.item.id, filenames, file_format, **kwargs)


class TestImportClassificationData(TestImportData):
    task = DOCUMENT_CLASSIFICATION

    def assert_examples(self, dataset):
        self.assertEqual(Example.objects.count(), len(dataset))
        for text, expected_labels in dataset:
            example = Example.objects.get(text=text)
            labels = set(cat.label.text for cat in example.categories.all())
            self.assertEqual(labels, set(expected_labels))

    def assert_parse_error(self, response):
        self.assertGreaterEqual(len(response["error"]), 1)
        self.assertEqual(Example.objects.count(), 0)
        self.assertEqual(CategoryType.objects.count(), 0)
        self.assertEqual(Category.objects.count(), 0)

    def test_jsonl(self):
        filename = "text_classification/example.jsonl"
        file_format = "JSONL"
        kwargs = {"column_label": "labels"}
        dataset = [("exampleA", ["positive"]), ("exampleB", ["positive", "negative"]), ("exampleC", [])]
        self.import_dataset(filename, file_format, kwargs)
        self.assert_examples(dataset)

    def test_csv(self):
        filename = "text_classification/example.csv"
        file_format = "CSV"
        dataset = [("exampleA", ["positive"]), ("exampleB", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_csv_out_of_order_columns(self):
        filename = "text_classification/example_out_of_order_columns.csv"
        file_format = "CSV"
        dataset = [("exampleA", ["positive"]), ("exampleB", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_fasttext(self):
        filename = "text_classification/example_fasttext.txt"
        file_format = "fastText"
        dataset = [("exampleA", ["positive"]), ("exampleB", ["positive", "negative"]), ("exampleC", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_excel(self):
        filename = "text_classification/example.xlsx"
        file_format = "Excel"
        dataset = [("exampleA", ["positive"]), ("exampleB", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_json(self):
        filename = "text_classification/example.json"
        file_format = "JSON"
        dataset = [("exampleA", ["positive"]), ("exampleB", ["positive", "negative"]), ("exampleC", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_textfile(self):
        filename = "example.txt"
        file_format = "TextFile"
        dataset = [("exampleA\nexampleB\n\nexampleC\n", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_textline(self):
        filename = "example.txt"
        file_format = "TextLine"
        dataset = [("exampleA", []), ("exampleB", []), ("exampleC", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_wrong_jsonl(self):
        filename = "text_classification/example.json"
        file_format = "JSONL"
        response = self.import_dataset(filename, file_format)
        self.assert_parse_error(response)

    def test_wrong_json(self):
        filename = "text_classification/example.jsonl"
        file_format = "JSON"
        response = self.import_dataset(filename, file_format)
        self.assert_parse_error(response)

    def test_wrong_excel(self):
        filename = "text_classification/example.jsonl"
        file_format = "Excel"
        response = self.import_dataset(filename, file_format)
        self.assert_parse_error(response)

    def test_wrong_csv(self):
        filename = "text_classification/example.jsonl"
        file_format = "CSV"
        response = self.import_dataset(filename, file_format)
        self.assert_parse_error(response)


class TestImportSequenceLabelingData(TestImportData):
    task = SEQUENCE_LABELING

    def assert_examples(self, dataset):
        self.assertEqual(Example.objects.count(), len(dataset))
        for text, expected_labels in dataset:
            example = Example.objects.get(text=text)
            labels = [[span.start_offset, span.end_offset, span.label.text] for span in example.spans.all()]
            self.assertEqual(labels, expected_labels)

    def assert_parse_error(self, response):
        self.assertGreaterEqual(len(response["error"]), 1)
        self.assertEqual(Example.objects.count(), 0)
        self.assertEqual(SpanType.objects.count(), 0)
        self.assertEqual(Span.objects.count(), 0)

    def test_jsonl(self):
        filename = "sequence_labeling/example.jsonl"
        file_format = "JSONL"
        dataset = [("exampleA", [[0, 1, "LOC"]]), ("exampleB", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_conll(self):
        filename = "sequence_labeling/example.conll"
        file_format = "CoNLL"
        dataset = [("JAPAN GET", [[0, 5, "LOC"]]), ("Nadim Ladki", [[0, 11, "PER"]])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_wrong_conll(self):
        filename = "sequence_labeling/example.jsonl"
        file_format = "CoNLL"
        response = self.import_dataset(filename, file_format)
        self.assert_parse_error(response)

    def test_jsonl_with_overlapping(self):
        filename = "sequence_labeling/example_overlapping.jsonl"
        file_format = "JSONL"
        response = self.import_dataset(filename, file_format)
        self.assertEqual(len(response["error"]), 1)


class TestImportSeq2seqData(TestImportData):
    task = SEQ2SEQ

    def assert_examples(self, dataset):
        self.assertEqual(Example.objects.count(), len(dataset))
        for text, expected_labels in dataset:
            example = Example.objects.get(text=text)
            labels = set(text_label.text for text_label in example.texts.all())
            self.assertEqual(labels, set(expected_labels))

    def test_jsonl(self):
        filename = "seq2seq/example.jsonl"
        file_format = "JSONL"
        dataset = [("exampleA", ["label1"]), ("exampleB", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_json(self):
        filename = "seq2seq/example.json"
        file_format = "JSON"
        dataset = [("exampleA", ["label1"]), ("exampleB", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)

    def test_csv(self):
        filename = "seq2seq/example.csv"
        file_format = "CSV"
        dataset = [("exampleA", ["label1"]), ("exampleB", [])]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)


class TestImportIntentDetectionAndSlotFillingData(TestImportData):
    task = INTENT_DETECTION_AND_SLOT_FILLING

    def assert_examples(self, dataset):
        self.assertEqual(Example.objects.count(), len(dataset))
        for text, expected_labels in dataset:
            example = Example.objects.get(text=text)
            cats = set(cat.label.text for cat in example.categories.all())
            entities = [(span.start_offset, span.end_offset, span.label.text) for span in example.spans.all()]
            self.assertEqual(cats, set(expected_labels["cats"]))
            self.assertEqual(entities, expected_labels["entities"])

    def test_entities_and_cats(self):
        filename = "intent/example.jsonl"
        file_format = "JSONL"
        dataset = [
            ("exampleA", {"cats": ["positive"], "entities": [(0, 1, "LOC")]}),
            ("exampleB", {"cats": ["positive"], "entities": []}),
            ("exampleC", {"cats": [], "entities": [(0, 1, "LOC")]}),
            ("exampleD", {"cats": [], "entities": []}),
        ]
        self.import_dataset(filename, file_format)
        self.assert_examples(dataset)


class TestImportImageClassificationData(TestImportData):
    task = IMAGE_CLASSIFICATION

    def test_example(self):
        filename = "images/1500x500.jpeg"
        file_format = "ImageFile"
        self.import_dataset(filename, file_format)
        self.assertEqual(Example.objects.count(), 1)
