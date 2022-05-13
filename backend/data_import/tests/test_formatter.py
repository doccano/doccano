import unittest
from unittest.mock import MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from data_import.pipeline.formatters import (
    DEFAULT_DATA_COLUMN,
    DataFormatter,
    LabelFormatter,
)
from data_import.pipeline.readers import (
    DEFAULT_LABEL_COLUMN,
    DEFAULT_TEXT_COLUMN,
    FILE_NAME_COLUMN,
    LINE_NUM_COLUMN,
    UPLOAD_NAME_COLUMN,
    UUID_COLUMN,
)


class TestLabelFormatter(unittest.TestCase):
    def setUp(self):
        self.label_column = "label"
        self.label_class = MagicMock
        self.label_class.parse = lambda x: x
        self.df = pd.DataFrame(
            [
                {LINE_NUM_COLUMN: 1, UUID_COLUMN: 1, self.label_column: ["A"]},
                {LINE_NUM_COLUMN: 2, UUID_COLUMN: 2, self.label_column: ["B", "C"]},
            ]
        )

    def test_format(self):
        label_formatter = LabelFormatter(column=self.label_column, label_class=self.label_class)
        df = label_formatter.format(self.df)
        expected_df = pd.DataFrame(
            [
                {UUID_COLUMN: 1, DEFAULT_LABEL_COLUMN: "A"},
                {UUID_COLUMN: 2, DEFAULT_LABEL_COLUMN: "B"},
                {UUID_COLUMN: 2, DEFAULT_LABEL_COLUMN: "C"},
            ]
        )
        assert_frame_equal(df, expected_df)

    def test_format_without_specified_column(self):
        label_formatter = LabelFormatter(column="invalid_column", label_class=self.label_class)
        with self.assertRaises(KeyError):
            label_formatter.format(self.df)

    def test_format_with_partially_correct_column(self):
        label_formatter = LabelFormatter(column=self.label_column, label_class=self.label_class)
        df = pd.DataFrame(
            [
                {LINE_NUM_COLUMN: 1, UUID_COLUMN: 1, self.label_column: ["A"]},
                {LINE_NUM_COLUMN: 2, UUID_COLUMN: 2, "invalid_column": ["B"]},
                {LINE_NUM_COLUMN: 3, UUID_COLUMN: 3},
            ]
        )
        df_label = label_formatter.format(df)
        expected_df = pd.DataFrame([{UUID_COLUMN: 1, DEFAULT_LABEL_COLUMN: "A"}])
        assert_frame_equal(df_label, expected_df)

    def test_format_with_invalid_label(self):
        label_class = MagicMock
        label_class.parse = lambda x: x if x else None
        label_formatter = LabelFormatter(column=self.label_column, label_class=label_class)
        df = pd.DataFrame(
            [
                {LINE_NUM_COLUMN: 1, UUID_COLUMN: 1, self.label_column: ["A"]},
                {LINE_NUM_COLUMN: 2, UUID_COLUMN: 2, self.label_column: [{}]},
            ]
        )
        df_label = label_formatter.format(df)
        expected_df = pd.DataFrame([{UUID_COLUMN: 1, DEFAULT_LABEL_COLUMN: "A"}])
        assert_frame_equal(df_label, expected_df)


class TestDataFormatter(unittest.TestCase):
    def setUp(self):
        self.data_column = "data"
        self.filename = "filename"
        self.upload_name = "upload_name"

    def test_format(self):
        data_class = MagicMock
        data_class.parse = lambda **kwargs: kwargs
        data_formatter = DataFormatter(column=self.data_column, data_class=data_class)
        df = pd.DataFrame(
            [
                {
                    LINE_NUM_COLUMN: 1,
                    UUID_COLUMN: 1,
                    self.data_column: "A",
                    FILE_NAME_COLUMN: self.filename,
                    UPLOAD_NAME_COLUMN: self.upload_name,
                },
            ]
        )
        df_data = data_formatter.format(df)
        expected_df = pd.DataFrame(
            [
                {
                    UUID_COLUMN: 1,
                    DEFAULT_DATA_COLUMN: {
                        UUID_COLUMN: 1,
                        DEFAULT_TEXT_COLUMN: "A",
                        "filename": self.filename,
                        "upload_name": self.upload_name,
                    },
                },
            ]
        )
        assert_frame_equal(df_data, expected_df)
