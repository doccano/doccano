import os
import pathlib
import shutil

from django.core.files import File
from django.test import TestCase, override_settings
from django_drf_filepond.models import StoredUpload, TemporaryUpload
from django_drf_filepond.utils import _get_file_id

from data_import.celery_tasks import import_dataset
from data_import.pipeline.catalog import RELATION_EXTRACTION
from examples.models import Example
from label_types.models import SpanType
from labels.models import Category, Span
from projects.models import ProjectType
from projects.tests.utils import prepare_project


@override_settings(MEDIA_ROOT=os.path.join(os.path.dirname(__file__), "data"))
class TestImportData(TestCase):
    task = "Any"
    annotation_class = Category

    def setUp(self):
        self.project = prepare_project(self.task)
        self.user = self.project.admin
        self.data_path = pathlib.Path(__file__).parent / "data"
        self.upload_id = _get_file_id()

    def tearDown(self):
        try:
            su = StoredUpload.objects.get(upload_id=self.upload_id)
            directory = pathlib.Path(su.get_absolute_file_path()).parent
            shutil.rmtree(directory)
        except StoredUpload.DoesNotExist:
            pass

    def import_dataset(self, filename, file_format, task, kwargs=None):
        file_path = str(self.data_path / filename)
        TemporaryUpload.objects.create(
            upload_id=self.upload_id,
            file_id="1",
            file=File(open(file_path, mode="rb"), filename.split("/")[-1]),
            upload_name=filename,
            upload_type="F",
        )
        upload_ids = [self.upload_id]
        kwargs = kwargs or {}
        return import_dataset(self.user.id, self.project.item.id, file_format, upload_ids, task, **kwargs)


@override_settings(MAX_UPLOAD_SIZE=0)
class TestMaxFileSize(TestImportData):
    task = ProjectType.DOCUMENT_CLASSIFICATION

    def test_jsonl(self):
        filename = "text_classification/example.jsonl"
        file_format = "JSONL"
        kwargs = {"column_label": "labels"}
        response = self.import_dataset(filename, file_format, self.task, kwargs)
        self.assertEqual(len(response["error"]), 1)
        self.assertIn("maximum file size", response["error"][0]["message"])


class TestInvalidFileFormat(TestImportData):
    task = ProjectType.DOCUMENT_CLASSIFICATION

    def test_invalid_file_format(self):
        filename = "text_classification/example.csv"
        file_format = "INVALID_FORMAT"
        response = self.import_dataset(filename, file_format, self.task)
        self.assertEqual(len(response["error"]), 1)


class TestImportClassificationData(TestImportData):
    task = ProjectType.DOCUMENT_CLASSIFICATION

    def assert_examples(self, dataset):
        with self.subTest():
            self.assertEqual(Example.objects.count(), len(dataset))
            for text, expected_labels in dataset:
                example = Example.objects.get(text=text)
                labels = set(cat.label.text for cat in example.categories.all())
                self.assertEqual(labels, set(expected_labels))

    def assert_parse_error(self, response):
        with self.subTest():
            self.assertGreaterEqual(len(response["error"]), 1)
            self.assertEqual(Example.objects.count(), 0)
            self.assertEqual(Category.objects.count(), 0)

    def test_jsonl(self):
        filename = "text_classification/example.jsonl"
        file_format = "JSONL"
        kwargs = {"column_label": "labels"}
        dataset = [("exampleA", ["positive"]), ("exampleB", ["positive", "negative"]), ("exampleC", [])]
        self.import_dataset(filename, file_format, self.task, kwargs)
        self.assert_examples(dataset)

    def test_csv(self):
        filename = "text_classification/example.csv"
        file_format = "CSV"
        dataset = [("exampleA", ["positive"]), ("exampleB", [])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_csv_out_of_order_columns(self):
        filename = "text_classification/example_out_of_order_columns.csv"
        file_format = "CSV"
        dataset = [("exampleA", ["positive"]), ("exampleB", [])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_fasttext(self):
        filename = "text_classification/example_fasttext.txt"
        file_format = "fastText"
        dataset = [("exampleA", ["positive"]), ("exampleB", ["positive", "negative"]), ("exampleC", [])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_excel(self):
        filename = "text_classification/example.xlsx"
        file_format = "Excel"
        dataset = [("exampleA", ["positive"]), ("exampleB", [])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_json(self):
        filename = "text_classification/example.json"
        file_format = "JSON"
        dataset = [("exampleA", ["positive"]), ("exampleB", ["positive", "negative"]), ("exampleC", [])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_textfile(self):
        filename = "example.txt"
        file_format = "TextFile"
        dataset = [("exampleA\nexampleB\n\nexampleC\n", [])]
        response = self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)
        self.assertEqual(len(response["error"]), 0)

    def test_textline(self):
        filename = "example.txt"
        file_format = "TextLine"
        dataset = [("exampleA", []), ("exampleB", []), ("exampleC", [])]
        response = self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)
        self.assertEqual(len(response["error"]), 1)

    def test_wrong_jsonl(self):
        filename = "text_classification/example.json"
        file_format = "JSONL"
        response = self.import_dataset(filename, file_format, self.task)
        self.assert_parse_error(response)

    def test_wrong_json(self):
        filename = "text_classification/example.jsonl"
        file_format = "JSON"
        response = self.import_dataset(filename, file_format, self.task)
        self.assert_parse_error(response)

    def test_wrong_excel(self):
        filename = "text_classification/example.jsonl"
        file_format = "Excel"
        response = self.import_dataset(filename, file_format, self.task)
        self.assert_parse_error(response)

    def test_wrong_csv(self):
        filename = "text_classification/example.jsonl"
        file_format = "CSV"
        response = self.import_dataset(filename, file_format, self.task)
        self.assert_parse_error(response)


class TestImportSequenceLabelingData(TestImportData):
    task = ProjectType.SEQUENCE_LABELING

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
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_conll(self):
        filename = "sequence_labeling/example.conll"
        file_format = "CoNLL"
        dataset = [("JAPAN GET", [[0, 5, "LOC"]]), ("Nadim Ladki", [[0, 11, "PER"]])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_wrong_conll(self):
        filename = "sequence_labeling/example.jsonl"
        file_format = "CoNLL"
        response = self.import_dataset(filename, file_format, self.task)
        self.assert_parse_error(response)

    def test_jsonl_with_overlapping(self):
        filename = "sequence_labeling/example_overlapping.jsonl"
        file_format = "JSONL"
        response = self.import_dataset(filename, file_format, self.task)
        self.assertEqual(len(response["error"]), 0)


class TestImportRelationExtractionData(TestImportData):
    task = ProjectType.SEQUENCE_LABELING

    def setUp(self):
        self.project = prepare_project(self.task, use_relation=True)
        self.user = self.project.admin
        self.data_path = pathlib.Path(__file__).parent / "data"
        self.upload_id = _get_file_id()

    def assert_examples(self, dataset):
        self.assertEqual(Example.objects.count(), len(dataset))
        for text, expected_spans in dataset:
            example = Example.objects.get(text=text)
            spans = [[span.start_offset, span.end_offset, span.label.text] for span in example.spans.all()]
            self.assertEqual(spans, expected_spans)
            self.assertEqual(example.relations.count(), 3)

    def assert_parse_error(self, response):
        self.assertGreaterEqual(len(response["error"]), 1)
        self.assertEqual(Example.objects.count(), 0)
        self.assertEqual(SpanType.objects.count(), 0)
        self.assertEqual(Span.objects.count(), 0)

    def test_jsonl(self):
        filename = "relation_extraction/example.jsonl"
        file_format = "JSONL"
        dataset = [
            (
                "Google was founded on September 4, 1998, by Larry Page and Sergey Brin.",
                [[0, 6, "ORG"], [22, 39, "DATE"], [44, 54, "PERSON"], [59, 70, "PERSON"]],
            ),
        ]
        self.import_dataset(filename, file_format, RELATION_EXTRACTION)
        self.assert_examples(dataset)


class TestImportSeq2seqData(TestImportData):
    task = ProjectType.SEQ2SEQ

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
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_json(self):
        filename = "seq2seq/example.json"
        file_format = "JSON"
        dataset = [("exampleA", ["label1"]), ("exampleB", [])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)

    def test_csv(self):
        filename = "seq2seq/example.csv"
        file_format = "CSV"
        dataset = [("exampleA", ["label1"]), ("exampleB", [])]
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)


class TestImportIntentDetectionAndSlotFillingData(TestImportData):
    task = ProjectType.INTENT_DETECTION_AND_SLOT_FILLING

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
        self.import_dataset(filename, file_format, self.task)
        self.assert_examples(dataset)


class TestImportImageClassificationData(TestImportData):
    task = ProjectType.IMAGE_CLASSIFICATION

    def test_example(self):
        filename = "images/1500x500.jpeg"
        file_format = "ImageFile"
        self.import_dataset(filename, file_format, self.task)
        self.assertEqual(Example.objects.count(), 1)


@override_settings(ENABLE_FILE_TYPE_CHECK=True)
class TestFileTypeChecking(TestImportData):
    task = ProjectType.IMAGE_CLASSIFICATION

    def test_example(self):
        filename = "images/example.ico"
        file_format = "ImageFile"
        response = self.import_dataset(filename, file_format, self.task)
        self.assertEqual(len(response["error"]), 1)
        self.assertIn("unexpected", response["error"][0]["message"])
