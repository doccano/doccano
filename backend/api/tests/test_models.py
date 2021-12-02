from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase, override_settings
from model_mommy import mommy

from ..models import (SEQUENCE_LABELING, Category, Label, Span, TextLabel,
                      generate_random_hex_color)
from .api.utils import prepare_project


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestTextClassificationProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('TextClassificationProject')

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, Category)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestSequenceLabelingProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('SequenceLabelingProject')

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, Span)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestSeq2seqProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('Seq2seqProject')

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, TextLabel)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestSpeech2textProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('Speech2textProject')

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, TextLabel)


class TestLabel(TestCase):

    def test_text_uniqueness(self):
        label = mommy.make('Label')
        mommy.make('Label', text=label.text)
        with self.assertRaises(IntegrityError):
            Label(project=label.project, text=label.text).save()

    def test_keys_uniqueness(self):
        label = mommy.make('Label', prefix_key='ctrl', suffix_key='a')
        with self.assertRaises(ValidationError):
            Label(project=label.project,
                  text='example',
                  prefix_key=label.prefix_key,
                  suffix_key=label.suffix_key).full_clean()

    def test_suffix_key_uniqueness(self):
        label = mommy.make('Label', prefix_key=None, suffix_key='a')
        with self.assertRaises(ValidationError):
            Label(project=label.project,
                  text='example',
                  prefix_key=label.prefix_key,
                  suffix_key=label.suffix_key).full_clean()

    def test_cannot_add_label_only_prefix_key(self):
        project = mommy.make('Project')
        label = Label(project=project,
                      text='example',
                      prefix_key='ctrl')
        with self.assertRaises(ValidationError):
            label.clean()

    def test_can_add_label_only_suffix_key(self):
        project = mommy.make('Project')
        label = Label(project=project,
                      text='example',
                      suffix_key='a')
        try:
            label.full_clean()
        except ValidationError:
            self.fail(msg=ValidationError)

    def test_can_add_label_suffix_key_with_prefix_key(self):
        project = mommy.make('Project')
        label = Label(project=project,
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
