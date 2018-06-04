import os

from django.test import TestCase, Client
from django.urls import reverse

from .models import Project, RawData, Label


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


class TestLabelAPI(TestCase):

    def test_get(self):
        client = Client()
        res = client.get(reverse('data_api', args=[1]))
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), dict)
        self.assertIn('data', res.json())
        self.assertEqual(res.json()['data'], [])

    def test_post(self):
        self.assertEqual(Label.objects.count(), 0)
        client = Client()
        res = client.post(reverse('label_api', args=[1]),
                          data={'text': 'label1', 'shortcut': 'k'})
        self.assertGreater(Label.objects.count(), 0)
        self.assertEqual(Label.objects.count(), 1)

    def test_put(self):
        self.assertEqual(Label.objects.count(), 0)
        client = Client()
        res = client.post(reverse('label_api', args=[1]),
                          data={'text': 'label1', 'shortcut': 'k'})
        self.assertEqual(Label.objects.count(), 1)
        prev_label = Label.objects.all()[0]
        text = 'neko'
        shortcut = 'P'

        res = client.put(reverse('label_api', args=[1]),
                            data={"id": prev_label.id, 'text': text, 'shortcut': shortcut})
        self.assertEqual(Label.objects.count(), 1)
        post_label = Label.objects.all()[0]
        self.assertEqual(prev_label.id, post_label.id)
        self.assertEqual(post_label.text, text)
        self.assertEqual(post_label.shortcut, shortcut)

    def test_delete(self):
        self.assertEqual(Label.objects.count(), 0)
        client = Client()
        res = client.post(reverse('label_api', args=[1]),
                          data={'text': 'label1', 'shortcut': 'k'})
        self.assertEqual(Label.objects.count(), 1)
        label_id = Label.objects.all()[0].id
        res = client.delete(reverse('label_api', args=[1]),
                            data={"id": label_id})
        self.assertEqual(Label.objects.count(), 0)
