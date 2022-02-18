import unittest
from typing import List, Optional

from data_import.pipeline import builders
from data_import.pipeline.data import TextData
from data_import.pipeline.exceptions import FileParseException
from data_import.pipeline.labels import CategoryLabel, SpanLabel


class TestColumnBuilder(unittest.TestCase):
    def assert_record(self, actual, expected):
        self.assertEqual(actual.data.text, expected["data"])
        self.assertEqual(actual.label, expected["label"])

    def create_record(self, row, data_column: builders.DataColumn, label_columns: Optional[List[builders.Column]]):
        builder = builders.ColumnBuilder(data_column=data_column, label_columns=label_columns)
        return builder.build(row, filename="", line_num=1)

    def test_can_load_default_column_names(self):
        row = {"text": "Text", "label": "Label"}
        data_column = builders.DataColumn("text", TextData)
        label_columns = [builders.LabelColumn("label", CategoryLabel)]
        actual = self.create_record(row, data_column, label_columns)
        expected = {"data": "Text", "label": [{"label": "Label"}]}
        self.assert_record(actual, expected)

    def test_can_specify_any_column_names(self):
        row = {"body": "Text", "star": 5}
        data_column = builders.DataColumn("body", TextData)
        label_columns = [builders.LabelColumn("star", CategoryLabel)]
        actual = self.create_record(row, data_column, label_columns)
        expected = {"data": "Text", "label": [{"label": "5"}]}
        self.assert_record(actual, expected)

    def test_can_load_only_text_column(self):
        row = {"text": "Text", "label": None}
        data_column = builders.DataColumn("text", TextData)
        label_columns = [builders.LabelColumn("label", CategoryLabel)]
        actual = self.create_record(row, data_column, label_columns)
        expected = {"data": "Text", "label": []}
        self.assert_record(actual, expected)

    def test_denies_no_data_column(self):
        row = {"label": "Label"}
        data_column = builders.DataColumn("text", TextData)
        label_columns = [builders.LabelColumn("label", CategoryLabel)]
        with self.assertRaises(FileParseException):
            self.create_record(row, data_column, label_columns)

    def test_denies_empty_text(self):
        row = {"text": "", "label": "Label"}
        data_column = builders.DataColumn("text", TextData)
        label_columns = [builders.LabelColumn("label", CategoryLabel)]
        with self.assertRaises(FileParseException):
            self.create_record(row, data_column, label_columns)

    def test_can_load_int_as_text(self):
        row = {"text": 5, "label": "Label"}
        data_column = builders.DataColumn("text", TextData)
        label_columns = [builders.LabelColumn("label", CategoryLabel)]
        actual = self.create_record(row, data_column, label_columns)
        expected = {"data": "5", "label": [{"label": "Label"}]}
        self.assert_record(actual, expected)

    def test_can_build_multiple_labels(self):
        row = {"text": "Text", "cats": ["Label"], "entities": [(0, 1, "LOC")]}
        data_column = builders.DataColumn("text", TextData)
        label_columns = [builders.LabelColumn("cats", CategoryLabel), builders.LabelColumn("entities", SpanLabel)]
        actual = self.create_record(row, data_column, label_columns)
        expected = {"data": "Text", "label": [{"label": "Label"}, {"label": "LOC", "start_offset": 0, "end_offset": 1}]}
        self.assert_record(actual, expected)
