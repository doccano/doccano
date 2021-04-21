import unittest

from ...views.upload.utils import append_field


class TestDatasetUtils(unittest.TestCase):

    def test_can_append_field(self):
        data = [
            {'label': 'A'},
            {'label': 'B'}
        ]
        append_field(data, project=1)
        expected = [
            {'label': 'A', 'project': 1},
            {'label': 'B', 'project': 1}
        ]
        self.assertEqual(data, expected)

    def test_can_append_field_to_nested_list(self):
        annotation = [
            [{'label': '18'}],
            [{'label': '7'}, {'label': '4'}]
        ]
        docs = list(range(len(annotation)))
        for a, d in zip(annotation, docs):
            append_field(a, document=d)
        expected = [
            [{'label': '18', 'document': 0}],
            [{'label': '7', 'document': 1}, {'label': '4', 'document': 1}]
        ]
        self.assertEqual(annotation, expected)
