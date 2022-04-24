import os
import zipfile

import pandas as pd
from django.test import TestCase, override_settings
from model_mommy import mommy

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


def read_zip_content(file):
    datasets = {}
    with zipfile.ZipFile(file) as z:
        for file in z.filelist:
            username = file.filename.split(".")[0]
            with z.open(file) as f:
                try:
                    df = pd.read_json(f, lines=True)
                except pd.errors.EmptyDataError:
                    continue
            datasets[username] = df.to_dict(orient="records")
    return datasets


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExport(TestCase):
    def export_dataset(self, confirmed_only=False):
        file = export_dataset(self.project.id, "JSONL", confirmed_only)
        if self.project.item.collaborative_annotation:
            dataset = pd.read_json(file, lines=True).to_dict(orient="records")
        else:
            dataset = read_zip_content(file)
        os.remove(file)
        return dataset


class TestExportCategory(TestExport):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(DOCUMENT_CLASSIFICATION, collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item, text="example1")
        self.example2 = mommy.make("ExportedExample", project=self.project.item, text="example2")
        self.category1 = mommy.make("ExportedCategory", example=self.example1, user=self.project.admin)
        self.category2 = mommy.make("ExportedCategory", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset()
        expected_datasets = {
            self.project.admin.username: [
                {**self.example1.to_dict(), "categories": [self.category1.to_string()]},
                {**self.example2.to_dict(), "categories": []},
            ],
            self.project.approver.username: [
                {**self.example1.to_dict(), "categories": []},
                {**self.example2.to_dict(), "categories": []},
            ],
            self.project.annotator.username: [
                {**self.example1.to_dict(), "categories": [self.category2.to_string()]},
                {**self.example2.to_dict(), "categories": []},
            ],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(datasets[username], dataset)

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset()
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
            },
            {**self.example2.to_dict(), "categories": []},
        ]
        self.assertEqual(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset(confirmed_only=True)
        expected_datasets = {
            self.project.admin.username: [{**self.example1.to_dict(), "categories": [self.category1.to_string()]}]
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(datasets[username], dataset)

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset(confirmed_only=True)
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
            }
        ]
        self.assertEqual(dataset, expected_dataset)


class TestExportSeq2seq(TestExport):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SEQ2SEQ, collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("ExportedExample", project=self.project.item, text="unconfirmed")
        self.text1 = mommy.make("TextLabel", example=self.example1, user=self.project.admin)
        self.text2 = mommy.make("TextLabel", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset()
        expected_datasets = {
            self.project.admin.username: [
                {**self.example1.to_dict(), "labels": [self.text1.text]},
                {**self.example2.to_dict(), "labels": []},
            ],
            self.project.approver.username: [
                {**self.example1.to_dict(), "labels": []},
                {**self.example2.to_dict(), "labels": []},
            ],
            self.project.annotator.username: [
                {**self.example1.to_dict(), "labels": [self.text2.text]},
                {**self.example2.to_dict(), "labels": []},
            ],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(datasets[username], dataset)

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset()
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "labels": sorted([self.text1.text, self.text2.text]),
            },
            {**self.example2.to_dict(), "labels": []},
        ]
        self.assertEqual(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset(confirmed_only=True)
        expected_datasets = {
            self.project.admin.username: [
                {**self.example1.to_dict(), "labels": [self.text1.text]},
            ],
            self.project.approver.username: [],
            self.project.annotator.username: [],
        }
        for username, dataset in datasets.items():
            self.assertEqual(dataset, expected_datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset(confirmed_only=True)
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "labels": sorted([self.text1.text, self.text2.text]),
            }
        ]
        self.assertEqual(dataset, expected_dataset)


class TestExportIntentDetectionAndSlotFilling(TestExport):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING, collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("ExportedExample", project=self.project.item, text="unconfirmed")
        self.category1 = mommy.make("ExportedCategory", example=self.example1, user=self.project.admin)
        self.category2 = mommy.make("ExportedCategory", example=self.example1, user=self.project.annotator)
        self.span = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.admin, start_offset=0, end_offset=1
        )
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset()
        expected_datasets = {
            self.project.admin.username: [
                {
                    **self.example1.to_dict(),
                    "entities": [list(self.span.to_tuple())],
                    "categories": [self.category1.to_string()],
                },
                {**self.example2.to_dict(), "entities": [], "categories": []},
            ],
            self.project.annotator.username: [
                {
                    **self.example1.to_dict(),
                    "entities": [],
                    "categories": [self.category2.to_string()],
                },
                {**self.example2.to_dict(), "entities": [], "categories": []},
            ],
            self.project.approver.username: [
                {**self.example1.to_dict(), "entities": [], "categories": []},
                {**self.example2.to_dict(), "entities": [], "categories": []},
            ],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset, datasets[username])

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset()
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "entities": [list(self.span.to_tuple())],
                "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
            },
            {**self.example2.to_dict(), "entities": [], "categories": []},
        ]
        self.assertEqual(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset(confirmed_only=True)
        expected_datasets = {
            self.project.admin.username: [
                {
                    **self.example1.to_dict(),
                    "entities": [list(self.span.to_tuple())],
                    "categories": [self.category1.to_string()],
                },
            ],
            self.project.annotator.username: [],
            self.project.approver.username: [],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset, datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset(confirmed_only=True)
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "entities": [list(self.span.to_tuple())],
                "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
            },
        ]
        self.assertEqual(dataset, expected_dataset)


class TestExportSequenceLabeling(TestExport):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SEQUENCE_LABELING, collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item, text="confirmed")
        self.span1 = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.admin, start_offset=0, end_offset=1
        )
        self.span2 = mommy.make(
            "ExportedSpan", example=self.example1, user=self.project.annotator, start_offset=1, end_offset=2
        )
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)
        self.example2 = mommy.make("ExportedExample", project=self.project.item, text="unconfirmed")

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset()
        expected_datasets = {
            self.project.admin.username: [
                {**self.example1.to_dict(), "entities": [list(self.span1.to_tuple())]},
                {**self.example2.to_dict(), "entities": []},
            ],
            self.project.annotator.username: [
                {**self.example1.to_dict(), "entities": [list(self.span2.to_tuple())]},
                {**self.example2.to_dict(), "entities": []},
            ],
            self.project.approver.username: [
                {**self.example1.to_dict(), "entities": []},
                {**self.example2.to_dict(), "entities": []},
            ],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset, datasets[username])

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset()
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "entities": [list(self.span1.to_tuple()), list(self.span2.to_tuple())],
            },
            {**self.example2.to_dict(), "entities": []},
        ]
        self.assertEqual(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset(confirmed_only=True)
        expected_datasets = {
            self.project.admin.username: [
                {**self.example1.to_dict(), "entities": [list(self.span1.to_tuple())]},
            ],
            self.project.annotator.username: [],
            self.project.approver.username: [],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(dataset, datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset(confirmed_only=True)
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "entities": [list(self.span1.to_tuple()), list(self.span2.to_tuple())],
            },
        ]
        self.assertEqual(dataset, expected_dataset)


class TestExportSpeechToText(TestExport):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SPEECH2TEXT, collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("ExportedExample", project=self.project.item, text="unconfirmed")
        self.text1 = mommy.make("TextLabel", example=self.example1, user=self.project.admin)
        self.text2 = mommy.make("TextLabel", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset()
        expected_datasets = {
            self.project.admin.username: [
                {**self.example1.to_dict(), "labels": [self.text1.text]},
                {**self.example2.to_dict(), "labels": []},
            ],
            self.project.approver.username: [
                {**self.example1.to_dict(), "labels": []},
                {**self.example2.to_dict(), "labels": []},
            ],
            self.project.annotator.username: [
                {**self.example1.to_dict(), "labels": [self.text2.text]},
                {**self.example2.to_dict(), "labels": []},
            ],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(datasets[username], dataset)

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset()
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "labels": sorted([self.text1.text, self.text2.text]),
            },
            {**self.example2.to_dict(), "labels": []},
        ]
        self.assertEqual(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset(confirmed_only=True)
        expected_datasets = {
            self.project.admin.username: [
                {**self.example1.to_dict(), "labels": [self.text1.text]},
            ],
            self.project.annotator.username: [],
            self.project.approver.username: [],
        }
        for username, dataset in datasets.items():
            self.assertEqual(dataset, expected_datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset(confirmed_only=True)
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "labels": sorted([self.text1.text, self.text2.text]),
            }
        ]
        self.assertEqual(dataset, expected_dataset)


class TestExportImageClassification(TestExport):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(IMAGE_CLASSIFICATION, collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item, text="confirmed")
        self.example2 = mommy.make("ExportedExample", project=self.project.item, text="unconfirmed")
        self.category1 = mommy.make("ExportedCategory", example=self.example1, user=self.project.admin)
        self.category2 = mommy.make("ExportedCategory", example=self.example1, user=self.project.annotator)
        mommy.make("ExampleState", example=self.example1, confirmed_by=self.project.admin)

    def test_unconfirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset()
        expected_datasets = {
            self.project.admin.username: [
                {
                    **self.example1.to_dict(),
                    "categories": [self.category1.to_string()],
                },
                {**self.example2.to_dict(), "categories": []},
            ],
            self.project.approver.username: [
                {**self.example1.to_dict(), "categories": []},
                {**self.example2.to_dict(), "categories": []},
            ],
            self.project.annotator.username: [
                {
                    **self.example1.to_dict(),
                    "categories": [self.category2.to_string()],
                },
                {**self.example2.to_dict(), "categories": []},
            ],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(datasets[username], dataset)

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset()
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
            },
            {**self.example2.to_dict(), "categories": []},
        ]
        self.assertEqual(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset(confirmed_only=True)
        expected_datasets = {
            self.project.admin.username: [{**self.example1.to_dict(), "categories": [self.category1.to_string()]}]
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(datasets[username], dataset)

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset(confirmed_only=True)
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "categories": sorted([self.category1.to_string(), self.category2.to_string()]),
            }
        ]
        self.assertEqual(dataset, expected_dataset)


class TestExportRelation(TestExport):
    def prepare_data(self, collaborative=False):
        self.project = prepare_project(SEQUENCE_LABELING, use_relation=True, collaborative_annotation=collaborative)
        self.example1 = mommy.make("ExportedExample", project=self.project.item, text="example")
        self.example2 = mommy.make("ExportedExample", project=self.project.item, text="unconfirmed")
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
        datasets = self.export_dataset()
        expected_datasets = {
            self.project.admin.username: [
                {
                    **self.example1.to_dict(),
                    "entities": [self.span1.to_dict(), self.span2.to_dict()],
                    "relations": [self.relation.to_dict()],
                },
                {**self.example2.to_dict(), "entities": [], "relations": []},
            ],
            self.project.annotator.username: [
                {
                    **self.example1.to_dict(),
                    "entities": [self.span3.to_dict()],
                    "relations": [],
                },
                {**self.example2.to_dict(), "entities": [], "relations": []},
            ],
            self.project.approver.username: [
                {**self.example1.to_dict(), "entities": [], "relations": []},
                {**self.example2.to_dict(), "entities": [], "relations": []},
            ],
        }
        for username, dataset in expected_datasets.items():
            self.assertEqual(datasets[username], dataset)

    def test_unconfirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset()
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "entities": [self.span1.to_dict(), self.span2.to_dict(), self.span3.to_dict()],
                "relations": [self.relation.to_dict()],
            },
            {**self.example2.to_dict(), "entities": [], "relations": []},
        ]
        self.assertEqual(dataset, expected_dataset)

    def test_confirmed_and_non_collaborative(self):
        self.prepare_data()
        datasets = self.export_dataset(confirmed_only=True)
        expected_datasets = {
            self.project.admin.username: [
                {
                    **self.example1.to_dict(),
                    "entities": [self.span1.to_dict(), self.span2.to_dict()],
                    "relations": [self.relation.to_dict()],
                },
            ],
            self.project.annotator.username: [],
            self.project.approver.username: [],
        }
        for username, dataset in datasets.items():
            self.assertEqual(dataset, expected_datasets[username])

    def test_confirmed_and_collaborative(self):
        self.prepare_data(collaborative=True)
        dataset = self.export_dataset(confirmed_only=True)
        expected_dataset = [
            {
                **self.example1.to_dict(),
                "entities": [self.span1.to_dict(), self.span2.to_dict(), self.span3.to_dict()],
                "relations": [self.relation.to_dict()],
            }
        ]
        self.assertEqual(dataset, expected_dataset)
