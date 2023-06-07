import uuid

from django.test import TestCase

from data_import.pipeline.examples import Examples
from examples.models import Example
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestExamples(TestCase):
    def setUp(self):
        self.project = prepare_project(ProjectType.DOCUMENT_CLASSIFICATION)
        self.example_uuid = uuid.uuid4()
        example = Example(uuid=self.example_uuid, text="A", project=self.project.item)
        self.examples = Examples([example])

    def test_save(self):
        self.examples.save()
        self.assertEqual(Example.objects.count(), 1)

    def test_getitem(self):
        self.examples.save()
        example = self.examples[self.example_uuid]
        self.assertEqual(example.uuid, self.example_uuid)
