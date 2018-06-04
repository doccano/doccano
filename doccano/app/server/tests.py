import os

from django.test import TestCase, Client
from django.urls import reverse

from .models import Project, RawData


class ProjectModelTest(TestCase):

    def test_string_representation(self):
        project = Project(name='my project', description='my description')
        self.assertEqual(str(project), project.name)


class TestRawDataAPI(TestCase):

    def test_get(self):
        client = Client()
        res = client.get(reverse('data_api', args=[1]))
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), dict)
        self.assertIn('data', res.json())
        self.assertEqual(res.json()['data'], [])

    def test_post(self):
        self.assertEqual(RawData.objects.count(), 0)

        filename = os.path.join(os.path.dirname(__file__), 'data/test.jsonl')
        client = Client()
        with open(filename) as f:
            client.post(reverse('data_api', args=[1]),
                        {'name': 'fred', 'attachment': f})

        self.assertGreater(RawData.objects.count(), 0)
