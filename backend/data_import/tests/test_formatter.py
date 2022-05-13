import unittest
from unittest.mock import MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from data_import.pipeline.formatters import LabelFormatter
from data_import.pipeline.readers import LINE_NUM_COLUMN


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.label_column = "label"
        self.label_class = MagicMock
        self.label_class.parse = lambda x: x
        self.df = pd.DataFrame(
            [
                {LINE_NUM_COLUMN: 1, self.label_column: ["A"]},
                {LINE_NUM_COLUMN: 2, self.label_column: ["B", "C"]},
            ]
        )

    def test_format(self):
        label_formatter = LabelFormatter(column=self.label_column, label_class=self.label_class)
        df = label_formatter.format(self.df)
        expected_df = pd.DataFrame(
            [
                {LINE_NUM_COLUMN: 1, self.label_column: "A"},
                {LINE_NUM_COLUMN: 2, self.label_column: "B"},
                {LINE_NUM_COLUMN: 2, self.label_column: "C"},
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
                {LINE_NUM_COLUMN: 1, self.label_column: ["A"]},
                {LINE_NUM_COLUMN: 2, "invalid_column": ["B"]},
                {LINE_NUM_COLUMN: 3},
            ]
        )
        df_label = label_formatter.format(df)
        expected_df = pd.DataFrame([{LINE_NUM_COLUMN: 1, self.label_column: "A"}])
        assert_frame_equal(df_label, expected_df)

    def test_format_with_invalid_label(self):
        label_class = MagicMock
        label_class.parse = lambda x: x if x else None
        label_formatter = LabelFormatter(column=self.label_column, label_class=label_class)
        df = pd.DataFrame(
            [
                {LINE_NUM_COLUMN: 1, self.label_column: ["A"]},
                {LINE_NUM_COLUMN: 2, self.label_column: [{}]},
            ]
        )
        df_label = label_formatter.format(df)
        expected_df = pd.DataFrame([{LINE_NUM_COLUMN: 1, self.label_column: "A"}])
        assert_frame_equal(df_label, expected_df)
