from django.test import TestCase
from model_mommy import mommy

from examples.models import ExampleState
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestExampleState(TestCase):
    def setUp(self):
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING)
        self.example = mommy.make("Example", project=self.project.item)
        self.other = mommy.make("Example", project=self.project.item)
        self.examples = self.project.item.examples.all()

    def test_initial_done(self):
        done = ExampleState.objects.count_done(self.examples)
        self.assertEqual(done, 0)

    def test_done_confirmed_by_user(self):
        mommy.make("ExampleState", example=self.example, confirmed_by=self.project.admin)
        done = ExampleState.objects.count_done(self.examples)
        self.assertEqual(done, 1)

    def test_done_confirmed_by_multiple_user(self):
        mommy.make("ExampleState", example=self.example, confirmed_by=self.project.admin)
        mommy.make("ExampleState", example=self.example, confirmed_by=self.project.approver)
        done = ExampleState.objects.count_done(self.examples)
        self.assertEqual(done, 1)

    def test_done_confirmed_by_different_example(self):
        mommy.make("ExampleState", example=self.example, confirmed_by=self.project.admin)
        mommy.make("ExampleState", example=self.other, confirmed_by=self.project.approver)
        done = ExampleState.objects.count_done(self.examples, self.project.admin)
        self.assertEqual(done, 1)

    def test_initial_user(self):
        progress = ExampleState.objects.measure_member_progress(self.examples, self.project.members)
        expected_progress = [{"user": member.username, "done": 0} for member in self.project.members]
        self.assertEqual(progress, {"total": 2, "progress": expected_progress})

    def test_user_count_after_confirmation(self):
        mommy.make("ExampleState", example=self.example, confirmed_by=self.project.admin)
        progress = ExampleState.objects.measure_member_progress(self.examples, self.project.members)
        expected_progress = [{"user": member.username, "done": 0} for member in self.project.members]
        expected_progress[0]["done"] = 1
        self.assertEqual(progress, {"total": 2, "progress": expected_progress})

    def test_user_count_after_multiple_user_confirmation(self):
        user1 = self.project.admin
        user2 = self.project.approver
        mommy.make("ExampleState", example=self.example, confirmed_by=user1)
        mommy.make("ExampleState", example=self.example, confirmed_by=user2)
        progress = ExampleState.objects.measure_member_progress(self.examples, self.project.members)
        expected_progress = [{"user": member.username, "done": 0} for member in self.project.members]
        expected_progress[0]["done"] = 1
        expected_progress[1]["done"] = 1
        self.assertEqual(progress["total"], 2)
        self.assertCountEqual(progress["progress"], expected_progress)


class TestExample(TestCase):
    def test_text_project_returns_text_as_data_property(self):
        project = prepare_project(ProjectType.SEQUENCE_LABELING)
        example = mommy.make("Example", project=project.item)
        self.assertEqual(example.text, example.data)

    def test_image_project_returns_filename_as_data_property(self):
        project = prepare_project(ProjectType.IMAGE_CLASSIFICATION)
        example = mommy.make("Example", project=project.item)
        self.assertEqual(str(example.filename), example.data)
