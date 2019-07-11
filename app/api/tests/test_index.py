from unittest import TestCase
from django.conf import settings
from ..index import DocumentIndex


class TestDocumentIndex(TestCase):
    def test__init__(self):
        settings.ELASTIC_SEARCH_INDEX = 'test'
        test_index = DocumentIndex()
        self.assertEqual(test_index._name, {
            'test'
        })

        settings.ELASTIC_SEARCH_INDEX = None
