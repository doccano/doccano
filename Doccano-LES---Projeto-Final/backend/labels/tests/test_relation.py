from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestRelationLabeling(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(ProjectType.SEQUENCE_LABELING)
        cls.example = mommy.make("Example", project=cls.project.item)
        cls.label_type = mommy.make("RelationType", project=cls.project.item)
        cls.user = cls.project.admin

    def test_can_annotate_relation(self):
        from_id = mommy.make("Span", example=self.example, start_offset=0, end_offset=1)
        to_id = mommy.make("Span", example=self.example, start_offset=1, end_offset=2)
        mommy.make("Relation", example=self.example, from_id=from_id, to_id=to_id)

    def test_cannot_annotate_relation_if_span_example_is_different(self):
        from_id = mommy.make("Span", example=self.example, start_offset=0, end_offset=1)
        to_id = mommy.make("Span", start_offset=1, end_offset=2)
        with self.assertRaises(ValidationError):
            mommy.make("Relation", example=self.example, from_id=from_id, to_id=to_id)

    def test_cannot_annotate_relation_if_relation_example_is_different_from_span_example(self):
        from_id = mommy.make("Span", example=self.example, start_offset=0, end_offset=1)
        to_id = mommy.make("Span", example=self.example, start_offset=1, end_offset=2)
        with self.assertRaises(ValidationError):
            mommy.make("Relation", from_id=from_id, to_id=to_id)
