from django.test import TestCase
from model_mommy import mommy

from examples.assignment.usecase import StrategyName, bulk_assign
from projects.models import Member, ProjectType
from projects.tests.utils import prepare_project


class TestBulkAssignment(TestCase):
    def setUp(self):
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING)
        self.member_ids = list(Member.objects.values_list("id", flat=True))
        self.example = mommy.make("Example", project=self.project.item)

    def test_raise_error_if_weights_is_invalid(self):
        with self.assertRaises(ValueError):
            bulk_assign(
                self.project.item.id, StrategyName.weighted_sequential, self.member_ids, [0] * len(self.member_ids)
            )

    def test_raise_error_if_passing_wrong_member_ids(self):
        with self.assertRaises(ValueError):
            bulk_assign(
                self.project.item.id,
                StrategyName.weighted_sequential,
                self.member_ids + [100],
                [0] * len(self.member_ids),
            )

    def test_assign_examples(self):
        bulk_assign(self.project.item.id, StrategyName.weighted_sequential, self.member_ids, [100, 0, 0])
        self.assertEqual(self.example.assignments.count(), 1)
        self.assertEqual(self.example.assignments.first().assignee, self.project.admin)
