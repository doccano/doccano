import unittest

from ...views.upload import builders
from ...views.upload.data import TextData
from ...views.upload.label import CategoryLabel


class TestColumnBuilder(unittest.TestCase):

    def assert_record(self, actual, expected):
        self.assertEqual(actual.data['text'], expected['data'])
        self.assertEqual(actual.label, expected['label'])

    def test_can_load_default_column_names(self):
        row = {'text': 'Text', 'label': 'Label'}
        builder = builders.ColumnBuilder(
            data_class=TextData,
            label_class=CategoryLabel,
            text_column='text',
            label_column='label'
        )
        actual = builder.build(row, filename='', line_num=1)
        expected = {'data': 'Text', 'label': [{'text': 'Label'}]}
        self.assert_record(actual, expected)

    def test_can_load_only_text_column(self):
        row = {'text': 'Text', 'label': None}
        builder = builders.ColumnBuilder(
            data_class=TextData,
            label_class=CategoryLabel,
            text_column='text',
            label_column='label'
        )
        actual = builder.build(row, filename='', line_num=1)
        expected = {'data': 'Text', 'label': []}
        self.assert_record(actual, expected)
