from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from api.models import (IMAGE_CLASSIFICATION, SEQUENCE_LABELING, CategoryType,
                        ExampleState, generate_random_hex_color)

from .api.utils import prepare_project


class TestLabel(TestCase):

    def test_deny_creating_same_text(self):
        label = mommy.make('CategoryType')
        with self.assertRaises(IntegrityError):
            mommy.make('CategoryType', project=label.project, text=label.text)

    def test_keys_uniqueness(self):
        label = mommy.make('CategoryType', prefix_key='ctrl', suffix_key='a')
        with self.assertRaises(ValidationError):
            CategoryType(project=label.project,
                         text='example',
                         prefix_key=label.prefix_key,
                         suffix_key=label.suffix_key).full_clean()

    def test_suffix_key_uniqueness(self):
        label = mommy.make('CategoryType', prefix_key=None, suffix_key='a')
        with self.assertRaises(ValidationError):
            CategoryType(project=label.project,
                         text='example',
                         prefix_key=label.prefix_key,
                         suffix_key=label.suffix_key).full_clean()

    def test_cannot_add_label_only_prefix_key(self):
        project = mommy.make('Project')
        label = CategoryType(project=project,
                             text='example',
                             prefix_key='ctrl')
        with self.assertRaises(ValidationError):
            label.clean()

    def test_can_add_label_only_suffix_key(self):
        project = mommy.make('Project')
        label = CategoryType(project=project, text='example', suffix_key='a')
        try:
            label.full_clean()
        except ValidationError:
            self.fail(msg=ValidationError)

    def test_can_add_label_suffix_key_with_prefix_key(self):
        project = mommy.make('Project')
        label = CategoryType(project=project,
                             text='example',
                             prefix_key='ctrl',
                             suffix_key='a')
        try:
            label.full_clean()
        except ValidationError:
            self.fail(msg=ValidationError)


class TestGeneratedColor(TestCase):

    def test_length(self):
        for i in range(100):
            color = generate_random_hex_color()
            self.assertEqual(len(color), 7)


class TestExampleState(TestCase):

    def setUp(self):
        self.project = prepare_project(SEQUENCE_LABELING)
        self.example = mommy.make('Example', project=self.project.item)
        self.other = mommy.make('Example', project=self.project.item)
        self.examples = self.project.item.examples.all()

    def test_initial_done(self):
        done = ExampleState.objects.count_done(self.examples)
        self.assertEqual(done, 0)

    def test_done_confirmed_by_user(self):
        mommy.make('ExampleState', example=self.example, confirmed_by=self.project.users[0])
        done = ExampleState.objects.count_done(self.examples)
        self.assertEqual(done, 1)

    def test_done_confirmed_by_multiple_user(self):
        mommy.make('ExampleState', example=self.example, confirmed_by=self.project.users[0])
        mommy.make('ExampleState', example=self.example, confirmed_by=self.project.users[1])
        done = ExampleState.objects.count_done(self.examples)
        self.assertEqual(done, 1)

    def test_done_confirmed_by_different_example(self):
        mommy.make('ExampleState', example=self.example, confirmed_by=self.project.users[0])
        mommy.make('ExampleState', example=self.other, confirmed_by=self.project.users[1])
        done = ExampleState.objects.count_done(self.examples, self.project.users[0])
        self.assertEqual(done, 1)

    def test_initial_user(self):
        progress = ExampleState.objects.measure_member_progress(self.examples, self.project.users)
        expected_progress = [{'user': user.username, 'done': 0} for user in self.project.users]
        self.assertEqual(progress, {'total': 2, 'progress': expected_progress})

    def test_user_count_after_confirmation(self):
        mommy.make('ExampleState', example=self.example, confirmed_by=self.project.users[0])
        progress = ExampleState.objects.measure_member_progress(self.examples, self.project.users)
        expected_progress = [{'user': user.username, 'done': 0} for user in self.project.users]
        expected_progress[0]['done'] = 1
        self.assertEqual(progress, {'total': 2, 'progress': expected_progress})

    def test_user_count_after_multiple_user_confirmation(self):
        user1 = self.project.users[0]
        user2 = self.project.users[1]
        mommy.make('ExampleState', example=self.example, confirmed_by=user1)
        mommy.make('ExampleState', example=self.example, confirmed_by=user2)
        progress = ExampleState.objects.measure_member_progress(self.examples, self.project.users)
        expected_progress = [{'user': user.username, 'done': 0} for user in self.project.users]
        expected_progress[0]['done'] = 1
        expected_progress[1]['done'] = 1
        self.assertEqual(progress, {'total': 2, 'progress': expected_progress})


class TestExample(TestCase):

    def test_text_project_returns_text_as_data_property(self):
        project = prepare_project(SEQUENCE_LABELING)
        example = mommy.make('Example', project=project.item)
        self.assertEqual(example.text, example.data)

    def test_image_project_returns_filename_as_data_property(self):
        project = prepare_project(IMAGE_CLASSIFICATION)
        example = mommy.make('Example', project=project.item)
        self.assertEqual(str(example.filename), example.data)
