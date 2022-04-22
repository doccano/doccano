import os
import zipfile

import numpy as np
import pandas as pd
from django.test import TestCase, override_settings
from model_mommy import mommy
from pandas.testing import assert_frame_equal

from ..celery_tasks import export_dataset
from projects.models import DOCUMENT_CLASSIFICATION
from projects.tests.utils import prepare_project


def read_zip_content(file):
    datasets = {}
    with zipfile.ZipFile(file) as z:
        for file in z.filelist:
            username = file.filename.split(".")[0]
            with z.open(file) as f:
                try:
                    df = pd.read_csv(f)
                except pd.errors.EmptyDataError:
                    continue
            datasets[username] = df
    return datasets


@override_settings(MEDIA_URL=os.path.dirname(__file__))
class TestExportTask(TestCase):
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
                [
                    {
                        "id": self.example1.id,
                        "data": self.example1.text,
                        "categories": self.category1.label.text,
                    }
                ]
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
