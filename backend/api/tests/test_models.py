from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from api.models import (SEQUENCE_LABELING, Category, CategoryType,
                        ExampleState, Span, SpanType, TextLabel,
                        generate_random_hex_color)

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


class TestCategory(TestCase):

    def test_uniqueness(self):
        a = mommy.make('Category')
        with self.assertRaises(IntegrityError):
            Category(example=a.example, user=a.user, label=a.label).save()


class TestSpan(TestCase):

    def setUp(self):
        self.project = prepare_project(SEQUENCE_LABELING, allow_overlapping=False)
        self.example = mommy.make('Example', project=self.project.item)
        self.user = self.project.users[0]

    def test_start_offset_is_not_negative(self):
        with self.assertRaises(IntegrityError):
            mommy.make('Span', start_offset=-1, end_offset=0)

    def test_end_offset_is_not_negative(self):
        with self.assertRaises(IntegrityError):
            mommy.make('Span', start_offset=-2, end_offset=-1)

    def test_start_offset_is_less_than_end_offset(self):
        with self.assertRaises(IntegrityError):
            mommy.make('Span', start_offset=0, end_offset=0)

    def test_unique_constraint(self):
        mommy.make('Span', example=self.example, start_offset=5, end_offset=10, user=self.user)
        mommy.make('Span', example=self.example, start_offset=0, end_offset=5, user=self.user)
        mommy.make('Span', example=self.example, start_offset=10, end_offset=15, user=self.user)

    def test_unique_constraint_violated(self):
        mommy.make('Span', example=self.example, start_offset=5, end_offset=10, user=self.user)
        spans = [(5, 10), (5, 11), (4, 10), (6, 9), (9, 15), (0, 6)]
        for start_offset, end_offset in spans:
            with self.assertRaises(ValidationError):
                mommy.make(
                    'Span',
                    example=self.example,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    user=self.user
                )

    def test_unique_constraint_if_overlapping_is_allowed(self):
        project = prepare_project(SEQUENCE_LABELING, allow_overlapping=True)
        example = mommy.make('Example', project=project.item)
        user = project.users[0]
        mommy.make('Span', example=example, start_offset=5, end_offset=10, user=user)
        spans = [(5, 10), (5, 11), (4, 10), (6, 9), (9, 15), (0, 6)]
        for start_offset, end_offset in spans:
            mommy.make('Span', example=example, start_offset=start_offset, end_offset=end_offset, user=user)

    def test_update(self):
        span = mommy.make('Span', example=self.example, start_offset=0, end_offset=5)
        span.end_offset = 6
        span.save()


class TestSpanWithoutCollaborativeMode(TestCase):

    def setUp(self):
        self.project = prepare_project(SEQUENCE_LABELING, False, allow_overlapping=False)
        self.example = mommy.make('Example', project=self.project.item)

    def test_allow_users_to_create_same_spans(self):
        mommy.make('Span', example=self.example, start_offset=5, end_offset=10, user=self.project.users[0])
        mommy.make('Span', example=self.example, start_offset=5, end_offset=10, user=self.project.users[1])


class TestSpanWithCollaborativeMode(TestCase):

    def test_deny_users_to_create_same_spans(self):
        project = prepare_project(SEQUENCE_LABELING, True, allow_overlapping=False)
        example = mommy.make('Example', project=project.item)
        mommy.make('Span', example=example, start_offset=5, end_offset=10, user=project.users[0])
        with self.assertRaises(ValidationError):
            mommy.make('Span', example=example, start_offset=5, end_offset=10, user=project.users[1])

    def test_allow_users_to_create_same_spans_if_overlapping_is_allowed(self):
        project = prepare_project(SEQUENCE_LABELING, True, allow_overlapping=True)
        example = mommy.make('Example', project=project.item)
        mommy.make('Span', example=example, start_offset=5, end_offset=10, user=project.users[0])
        mommy.make('Span', example=example, start_offset=5, end_offset=10, user=project.users[1])


class TestSeq2seqAnnotation(TestCase):

    def test_uniqueness(self):
        a = mommy.make('TextLabel')
        with self.assertRaises(IntegrityError):
            TextLabel(example=a.example,
                      user=a.user,
                      text=a.text).save()


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


class TestLabelDistribution(TestCase):

    def setUp(self):
        self.project = prepare_project(SEQUENCE_LABELING, allow_overlapping=False)
        self.example = mommy.make('Example', project=self.project.item)
        self.user = self.project.users[0]

    def test_calc_label_distribution(self):
        label_a = mommy.make('SpanType', text='labelA', project=self.project.item)
        label_b = mommy.make('SpanType', text='labelB', project=self.project.item)
        mommy.make('Span', example=self.example, start_offset=5, end_offset=10, user=self.user, label=label_a)
        mommy.make('Span', example=self.example, start_offset=10, end_offset=15, user=self.user, label=label_b)
        distribution = Span.objects.calc_label_distribution(
            examples=self.project.item.examples.all(),
            members=self.project.users,
            labels=SpanType.objects.all()
        )
        expected = {user.username: {label.text: 0 for label in SpanType.objects.all()} for user in self.project.users}
        expected[self.user.username][label_a.text] = 1
        expected[self.user.username][label_b.text] = 1
        self.assertEqual(distribution, expected)
