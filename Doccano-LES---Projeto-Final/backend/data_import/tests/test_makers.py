import uuid

import pandas as pd
from django.test import TestCase

from data_import.pipeline.data import TextData
from data_import.pipeline.label import CategoryLabel
from data_import.pipeline.makers import ExampleMaker, LabelMaker
from data_import.pipeline.readers import (
    FILE_NAME_COLUMN,
    LINE_NUMBER_COLUMN,
    UPLOAD_NAME_COLUMN,
    UUID_COLUMN,
)
from projects.tests.utils import prepare_project


class TestExamplesMaker(TestCase):
    def setUp(self):
        self.project = prepare_project()
        self.label_column = "label"
        self.text_column = "text"
        self.record = {
            LINE_NUMBER_COLUMN: 1,
            UUID_COLUMN: uuid.uuid4(),
            FILE_NAME_COLUMN: "file1",
            UPLOAD_NAME_COLUMN: "upload1",
            self.text_column: "text1",
            self.label_column: ["A"],
        }
        self.maker = ExampleMaker(self.project.item, TextData, self.text_column, [self.label_column])

    def test_make_examples(self):
        df = pd.DataFrame([self.record])
        examples = self.maker.make(df)
        self.assertEqual(len(examples), 1)

    def test_check_column_existence(self):
        self.record.pop(self.text_column)
        df = pd.DataFrame([self.record])
        examples = self.maker.make(df)
        self.assertEqual(len(examples), 0)
        self.assertEqual(len(self.maker.errors), 1)

    def test_empty_text_raises_error(self):
        self.record[self.text_column] = ""
        df = pd.DataFrame([self.record])
        examples = self.maker.make(df)
        self.assertEqual(len(examples), 0)
        self.assertEqual(len(self.maker.errors), 1)


class TestLabelFormatter(TestCase):
    def setUp(self):
        self.label_column = "label"
        self.label_class = CategoryLabel
        self.df = pd.DataFrame(
            [
                {LINE_NUMBER_COLUMN: 1, UUID_COLUMN: uuid.uuid4(), self.label_column: ["A"]},
                {LINE_NUMBER_COLUMN: 2, UUID_COLUMN: uuid.uuid4(), self.label_column: ["B", "C"]},
            ]
        )

    def test_make(self):
        label_maker = LabelMaker(column=self.label_column, label_class=self.label_class)
        labels = label_maker.make(self.df)
        self.assertEqual(len(labels), 3)
        with self.subTest():
            for label, expected in zip(labels, ["A", "B", "C"]):
                self.assertEqual(getattr(label, "label"), expected)

    def test_format_without_specified_column(self):
        label_maker = LabelMaker(column="invalid_column", label_class=self.label_class)
        with self.assertRaises(KeyError):
            label_maker.make(self.df)

    def test_format_with_partially_correct_column(self):
        label_maker = LabelMaker(column=self.label_column, label_class=self.label_class)
        df = pd.DataFrame(
            [
                {LINE_NUMBER_COLUMN: 1, UUID_COLUMN: uuid.uuid4(), self.label_column: ["A"]},
                {LINE_NUMBER_COLUMN: 2, UUID_COLUMN: uuid.uuid4(), "invalid_column": ["B"]},
                {LINE_NUMBER_COLUMN: 3, UUID_COLUMN: uuid.uuid4()},
                {LINE_NUMBER_COLUMN: 3, UUID_COLUMN: uuid.uuid4(), self.label_column: [{}]},
            ]
        )
        labels = label_maker.make(df)
        self.assertEqual(len(labels), 1)
