import os
import zipfile

import numpy as np
import pandas as pd
from django.test import TestCase, override_settings
from model_mommy import mommy
from pandas.testing import assert_frame_equal

from ..celery_tasks import export_dataset
from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
)
from projects.tests.utils import prepare_project


def read_zip_content(file, file_format="csv"):
    datasets = {}
    with zipfile.ZipFile(file) as z:
        for file in z.filelist:
            username = file.filename.split(".")[0]
            with z.open(file) as f:
                try:
                    if file_format == "csv":
                        df = pd.read_csv(f)
                    elif file_format == "json":
                        df = pd.read_json(f)
                    elif file_format == "jsonl":
                        df = pd.read_json(f, lines=True)
                except pd.errors.EmptyDataError:
                    continue
            datasets[username] = df
    return datasets


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportCategory(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(DOCUMENT_CLASSIFICATION, collaborative_annotation=collaborative)
        self.example1 = mommy.make("Example", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("Example", project=self.project.item, text="unconfirmed")
        self.category1 = mommy.make("Category", example=self.example1, user=self.project.admin)
        self.category2 = mommy.make("Category", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "CSV", False)
        datasets = read_zip_content(file)
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "categories": self.category1.label.text},
                    {"id": self.example2.id, "data": self.example2.text, "categories": np.nan},
                ]
            ),
            self.project.approver.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "categories": np.nan},
                    {"id": self.example2.id, "data": self.example2.text, "categories": np.nan},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "categories": self.category2.label.text},
                    {"id": self.example2.id, "data": self.example2.text, "categories": np.nan},
                ]
            ),
        }
        for username, dataset in expected_datasets.items():
            assert_frame_equal(dataset, datasets[username])

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "CSV", False)
        dataset = pd.read_csv(file)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "categories": "#".join(sorted([self.category1.label.text, self.category2.label.text])),
                },
                {"id": self.example2.id, "data": self.example2.text, "categories": np.nan},
            ]
        )
        assert_frame_equal(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "CSV", True)
        datasets = read_zip_content(file)
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [{"id": self.example1.id, "data": self.example1.text, "categories": self.category1.label.text}]
            )
        }
        for username, dataset in expected_datasets.items():
            assert_frame_equal(dataset, datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "CSV", True)
        dataset = pd.read_csv(file)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "categories": "#".join(sorted([self.category1.label.text, self.category2.label.text])),
                }
            ]
        )
        assert_frame_equal(dataset, expected_dataset)


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportSeq2seq(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SEQ2SEQ, collaborative_annotation=collaborative)
        self.example1 = mommy.make("Example", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("Example", project=self.project.item, text="unconfirmed")
        self.text1 = mommy.make("TextLabel", example=self.example1, user=self.project.admin)
        self.text2 = mommy.make("TextLabel", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "CSV", False)
        datasets = read_zip_content(file)
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "labels": self.text1.text},
                    {"id": self.example2.id, "data": self.example2.text, "labels": np.nan},
                ]
            ),
            self.project.approver.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "labels": np.nan},
                    {"id": self.example2.id, "data": self.example2.text, "labels": np.nan},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "labels": self.text2.text},
                    {"id": self.example2.id, "data": self.example2.text, "labels": np.nan},
                ]
            ),
        }
        for username, dataset in expected_datasets.items():
            assert_frame_equal(dataset, datasets[username])

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "CSV", False)
        dataset = pd.read_csv(file)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "labels": "#".join(sorted([self.text1.text, self.text2.text])),
                },
                {"id": self.example2.id, "data": self.example2.text, "labels": np.nan},
            ]
        )
        assert_frame_equal(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "CSV", True)
        datasets = read_zip_content(file)
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "labels": self.text1.text},
                ]
            )
        }
        for username, dataset in datasets.items():
            assert_frame_equal(dataset, expected_datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "CSV", True)
        dataset = pd.read_csv(file)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "labels": "#".join(sorted([self.text1.text, self.text2.text])),
                }
            ]
        )
        assert_frame_equal(dataset, expected_dataset)


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportIntentDetectionAndSlotFilling(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING, collaborative_annotation=collaborative)
        self.example1 = mommy.make("Example", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("Example", project=self.project.item, text="unconfirmed")
        self.category1 = mommy.make("ExportedCategory", example=self.example1, user=self.project.admin)
        self.category2 = mommy.make("ExportedCategory", example=self.example1, user=self.project.annotator)
        self.span = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.admin, start_offset=0, end_offset=1
        )
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", False)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)

        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.text,
                        "entities": [list(self.span.to_tuple())],
                        "categories": [self.category1.to_string()],
                    },
                    {"id": self.example2.id, "data": self.example2.text, "entities": [], "categories": []},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.text,
                        "entities": [],
                        "categories": [self.category2.to_string()],
                    },
                    {"id": self.example2.id, "data": self.example2.text, "entities": [], "categories": []},
                ]
            ),
            self.project.approver.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "entities": [], "categories": []},
                    {"id": self.example2.id, "data": self.example2.text, "entities": [], "categories": []},
                ]
            ),
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset.to_dict(), datasets[username].to_dict())

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", False)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "entities": [list(self.span.to_tuple())],
                    "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
                },
                {"id": self.example2.id, "data": self.example2.text, "entities": [], "categories": []},
            ]
        )
        self.assertEqual(dataset.to_dict(), expected_dataset.to_dict())

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", True)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)

        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.text,
                        "entities": [list(self.span.to_tuple())],
                        "categories": [self.category1.to_string()],
                    },
                ]
            ),
            self.project.annotator.username: pd.DataFrame(),
            self.project.approver.username: pd.DataFrame(),
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset.to_dict(), datasets[username].to_dict())

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", True)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "entities": [list(self.span.to_tuple())],
                    "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
                },
            ]
        )
        self.assertEqual(dataset.to_dict(), expected_dataset.to_dict())


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportSequenceLabeling(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SEQUENCE_LABELING, collaborative_annotation=collaborative)
        self.example1 = mommy.make("Example", project=self.project.item, text="confirmed")
        self.span1 = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.admin, start_offset=0, end_offset=1
        )
        self.span2 = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.annotator, start_offset=1, end_offset=2
        )
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)
        self.example2 = mommy.make("Example", project=self.project.item, text="unconfirmed")

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", False)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)

        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "entities": [list(self.span1.to_tuple())]},
                    {"id": self.example2.id, "data": self.example2.text, "entities": []},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "entities": [list(self.span2.to_tuple())]},
                    {"id": self.example2.id, "data": self.example2.text, "entities": []},
                ]
            ),
            self.project.approver.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "entities": []},
                    {"id": self.example2.id, "data": self.example2.text, "entities": []},
                ]
            ),
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset.to_dict(), datasets[username].to_dict())

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", False)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "entities": [self.span1.to_tuple(), self.span2.to_tuple()],
                },
                {"id": self.example2.id, "data": self.example2.text, "entities": []},
            ]
        )
        assert_frame_equal(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", True)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)

        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "entities": [list(self.span1.to_tuple())]},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(),
            self.project.approver.username: pd.DataFrame(),
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset.to_dict(), datasets[username].to_dict())

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", True)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "entities": [self.span1.to_tuple(), self.span2.to_tuple()],
                },
            ]
        )
        assert_frame_equal(dataset, expected_dataset)


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportSpeechToText(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SPEECH2TEXT, collaborative_annotation=collaborative)
        self.example1 = mommy.make("Example", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("Example", project=self.project.item, text="unconfirmed")
        self.text1 = mommy.make("TextLabel", example=self.example1, user=self.project.admin)
        self.text2 = mommy.make("TextLabel", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", False)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.upload_name, "labels": [self.text1.text]},
                    {"id": self.example2.id, "data": self.example2.upload_name, "labels": []},
                ]
            ),
            self.project.approver.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.upload_name, "labels": []},
                    {"id": self.example2.id, "data": self.example2.upload_name, "labels": []},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.upload_name, "labels": [self.text2.text]},
                    {"id": self.example2.id, "data": self.example2.upload_name, "labels": []},
                ]
            ),
        }
        for username, dataset in expected_datasets.items():
            assert_frame_equal(dataset, datasets[username])

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", False)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.upload_name,
                    "labels": sorted([self.text1.text, self.text2.text]),
                },
                {"id": self.example2.id, "data": self.example2.upload_name, "labels": []},
            ]
        )
        assert_frame_equal(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", True)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.upload_name, "labels": [self.text1.text]},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(),
            self.project.approver.username: pd.DataFrame(),
        }
        for username, dataset in datasets.items():
            self.assertEqual(dataset.to_dict(), expected_datasets[username].to_dict())

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", True)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.upload_name,
                    "labels": sorted([self.text1.text, self.text2.text]),
                }
            ]
        )
        assert_frame_equal(dataset, expected_dataset)


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportImageClassification(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(IMAGE_CLASSIFICATION, collaborative_annotation=collaborative)
        self.example1 = mommy.make("Example", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("Example", project=self.project.item, text="unconfirmed")
        self.category1 = mommy.make("Category", example=self.example1, user=self.project.admin)
        self.category2 = mommy.make("Category", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", False)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.upload_name,
                        "categories": [self.category1.label.text],
                    },
                    {"id": self.example2.id, "data": self.example2.upload_name, "categories": []},
                ]
            ),
            self.project.approver.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.upload_name, "categories": []},
                    {"id": self.example2.id, "data": self.example2.upload_name, "categories": []},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.upload_name,
                        "categories": [self.category2.label.text],
                    },
                    {"id": self.example2.id, "data": self.example2.upload_name, "categories": []},
                ]
            ),
        }
        for username, dataset in expected_datasets.items():
            assert_frame_equal(dataset, datasets[username])

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", False)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.upload_name,
                    "categories": sorted([self.category1.label.text, self.category2.label.text]),
                },
                {"id": self.example2.id, "data": self.example2.upload_name, "categories": []},
            ]
        )
        assert_frame_equal(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", True)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)
        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [{"id": self.example1.id, "data": self.example1.upload_name, "categories": [self.category1.label.text]}]
            )
        }
        for username, dataset in expected_datasets.items():
            assert_frame_equal(dataset, datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", True)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.upload_name,
                    "categories": sorted([self.category1.label.text, self.category2.label.text]),
                }
            ]
        )
        assert_frame_equal(dataset, expected_dataset)


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportRelation(TestCase):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SEQUENCE_LABELING, use_relation=True, collaborative_annotation=collaborative)
        self.example1 = mommy.make("Example", project=self.project.item, text="example")
        self.example2 = mommy.make("Example", project=self.project.item, text="unconfirmed")
        self.span1 = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.admin, start_offset=0, end_offset=1
        )
        self.span2 = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.admin, start_offset=1, end_offset=2
        )
        self.span3 = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.annotator, start_offset=2, end_offset=3
        )
        self.relation = mommy.make(
            "ExportedRelation", from_id=self.span1, to_id=self.span2, example=self.example1, user=self.project.admin
        )
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", False)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)

        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.text,
                        "entities": [self.span1.to_dict(), self.span2.to_dict()],
                        "relations": [self.relation.to_dict()],
                    },
                    {"id": self.example2.id, "data": self.example2.text, "entities": [], "relations": []},
                ]
            ),
            self.project.annotator.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.text,
                        "entities": [self.span3.to_dict()],
                        "relations": [],
                    },
                    {"id": self.example2.id, "data": self.example2.text, "entities": [], "relations": []},
                ]
            ),
            self.project.approver.username: pd.DataFrame(
                [
                    {"id": self.example1.id, "data": self.example1.text, "entities": [], "relations": []},
                    {"id": self.example2.id, "data": self.example2.text, "entities": [], "relations": []},
                ]
            ),
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset.to_dict(), datasets[username].to_dict())

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", False)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "entities": [self.span1.to_dict(), self.span2.to_dict(), self.span3.to_dict()],
                    "relations": [self.relation.to_dict()],
                },
                {"id": self.example2.id, "data": self.example2.text, "entities": [], "relations": []},
            ]
        )
        assert_frame_equal(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        file = export_dataset(self.project.id, "JSONL", True)
        datasets = read_zip_content(file, "jsonl")
        os.remove(file)

        expected_datasets = {
            self.project.admin.username: pd.DataFrame(
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.text,
                        "entities": [self.span1.to_dict(), self.span2.to_dict()],
                        "relations": [self.relation.to_dict()],
                    },
                ]
            ),
            self.project.annotator.username: pd.DataFrame(),
            self.project.approver.username: pd.DataFrame(),
        }
        for username, dataset in datasets.items():
            self.assertEqual(dataset.to_dict(), expected_datasets[username].to_dict())

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        file = export_dataset(self.project.id, "JSONL", True)
        dataset = pd.read_json(file, lines=True)
        os.remove(file)
        expected_dataset = pd.DataFrame(
            [
                {
                    "id": self.example1.id,
                    "data": self.example1.text,
                    "entities": [self.span1.to_dict(), self.span2.to_dict(), self.span3.to_dict()],
                    "relations": [self.relation.to_dict()],
                }
            ]
        )
        assert_frame_equal(dataset, expected_dataset)
