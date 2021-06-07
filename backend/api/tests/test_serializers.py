from rest_framework.test import APITestCase

from ..serializers import ExampleSerializer
from .api.utils import make_doc, make_example_state, prepare_project


class TestExampleStateSerializer(APITestCase):

    def setUp(self):
        self.project = prepare_project(task='DocumentClassification')
        self.example = make_doc(self.project.item)

    def test_in_is_confirmed(self):
        serializer = ExampleSerializer(instance=self.example)
        self.assertIn('is_confirmed', serializer.data)

    def test_is_not_confirmed(self):
        serializer = ExampleSerializer(instance=self.example)
        is_confirmed = serializer.data['is_confirmed']
        self.assertFalse(is_confirmed)

    def test_is_confirmed(self):
        make_example_state(self.example, self.project.users[0])
        serializer = ExampleSerializer(instance=self.example)
        is_confirmed = serializer.data['is_confirmed']
        self.assertTrue(is_confirmed)
