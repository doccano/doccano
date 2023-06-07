import abc

from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from label_types.models import SpanType
from labels.models import Span
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestSpanLabeling(abc.ABC, TestCase):
    overlapping = False
    collaborative = False

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(
            ProjectType.SEQUENCE_LABELING, allow_overlapping=cls.overlapping, collaborative_annotation=cls.collaborative
        )
        cls.example = mommy.make("Example", project=cls.project.item)
        cls.label_type = mommy.make("SpanType", project=cls.project.item)
        cls.user = cls.project.admin
        cls.another_user = cls.project.approver
        cls.span = Span(example=cls.example, label=cls.label_type, user=cls.user, start_offset=0, end_offset=5)

    def test_can_annotate_span_to_unannotated_data(self):
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)


class NonCollaborativeMixin:
    def test_allow_another_user_to_annotate_same_span(self):
        mommy.make(
            "Span",
            example=self.example,
            label=self.label_type,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)


class TestNonOverlappingSpanLabeling(TestSpanLabeling, NonCollaborativeMixin):
    overlapping = False
    collaborative = False

    def test_cannot_annotate_same_span_to_annotated_data(self):
        mommy.make(
            "Span",
            example=self.example,
            label=self.label_type,
            user=self.user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertFalse(can_annotate)

    def test_cannot_annotate_different_span_type_to_annotated_data(self):
        mommy.make(
            "Span",
            example=self.example,
            user=self.user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertFalse(can_annotate)


class TestOverlappingSpanLabeling(TestSpanLabeling, NonCollaborativeMixin):
    overlapping = True
    collaborative = False

    def test_can_annotate_same_span_to_annotated_data(self):
        mommy.make(
            "Span",
            example=self.example,
            label=self.label_type,
            user=self.user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)


class TestCollaborativeNonOverlappingSpanLabeling(TestSpanLabeling):
    overlapping = False
    collaborative = True

    def test_deny_another_user_to_annotate_same_span_type(self):
        mommy.make(
            "Span",
            example=self.example,
            label=self.label_type,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertFalse(can_annotate)

    def test_deny_another_user_to_annotate_different_span_type(self):
        mommy.make(
            "Span",
            example=self.example,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertFalse(can_annotate)


class TestCollaborativeOverlappingSpanLabeling(TestSpanLabeling):
    overlapping = True
    collaborative = True

    def test_allow_another_user_to_annotate_same_span(self):
        mommy.make(
            "Span",
            example=self.example,
            label=self.label_type,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)


class TestSpan(TestCase):
    def setUp(self):
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING, allow_overlapping=False)
        self.example = mommy.make("Example", project=self.project.item)
        self.user = self.project.admin

    def test_start_offset_is_not_negative(self):
        with self.assertRaises(ValidationError):
            mommy.make("Span", start_offset=-1, end_offset=0)

    def test_end_offset_is_not_negative(self):
        with self.assertRaises(ValidationError):
            mommy.make("Span", start_offset=-2, end_offset=-1)

    def test_start_offset_is_less_than_end_offset(self):
        with self.assertRaises(ValidationError):
            mommy.make("Span", start_offset=0, end_offset=0)

    def test_unique_constraint(self):
        mommy.make("Span", example=self.example, start_offset=5, end_offset=10, user=self.user)
        mommy.make("Span", example=self.example, start_offset=0, end_offset=5, user=self.user)
        mommy.make("Span", example=self.example, start_offset=10, end_offset=15, user=self.user)

    def test_unique_constraint_violated(self):
        mommy.make("Span", example=self.example, start_offset=5, end_offset=10, user=self.user)
        spans = [(5, 10), (5, 11), (4, 10), (6, 9), (9, 15), (0, 6)]
        for start_offset, end_offset in spans:
            with self.assertRaises(ValidationError):
                mommy.make(
                    "Span", example=self.example, start_offset=start_offset, end_offset=end_offset, user=self.user
                )

    def test_unique_constraint_if_overlapping_is_allowed(self):
        project = prepare_project(ProjectType.SEQUENCE_LABELING, allow_overlapping=True)
        example = mommy.make("Example", project=project.item)
        user = project.admin
        mommy.make("Span", example=example, start_offset=5, end_offset=10, user=user)
        spans = [(5, 10), (5, 11), (4, 10), (6, 9), (9, 15), (0, 6)]
        for start_offset, end_offset in spans:
            mommy.make("Span", example=example, start_offset=start_offset, end_offset=end_offset, user=user)

    def test_update(self):
        span = mommy.make("Span", example=self.example, start_offset=0, end_offset=5)
        span.end_offset = 6
        span.save()


class TestSpanWithoutCollaborativeMode(TestCase):
    def setUp(self):
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING, False, allow_overlapping=False)
        self.example = mommy.make("Example", project=self.project.item)

    def test_allow_users_to_create_same_spans(self):
        mommy.make("Span", example=self.example, start_offset=5, end_offset=10, user=self.project.admin)
        mommy.make("Span", example=self.example, start_offset=5, end_offset=10, user=self.project.approver)


class TestSpanWithCollaborativeMode(TestCase):
    def test_deny_users_to_create_same_spans(self):
        project = prepare_project(ProjectType.SEQUENCE_LABELING, True, allow_overlapping=False)
        example = mommy.make("Example", project=project.item)
        mommy.make("Span", example=example, start_offset=5, end_offset=10, user=project.admin)
        with self.assertRaises(ValidationError):
            mommy.make("Span", example=example, start_offset=5, end_offset=10, user=project.approver)

    def test_allow_users_to_create_same_spans_if_overlapping_is_allowed(self):
        project = prepare_project(ProjectType.SEQUENCE_LABELING, True, allow_overlapping=True)
        example = mommy.make("Example", project=project.item)
        mommy.make("Span", example=example, start_offset=5, end_offset=10, user=project.admin)
        mommy.make("Span", example=example, start_offset=5, end_offset=10, user=project.approver)


class TestLabelDistribution(TestCase):
    def setUp(self):
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING, allow_overlapping=False)
        self.example = mommy.make("Example", project=self.project.item)
        self.user = self.project.admin

    def test_calc_label_distribution(self):
        label_a = mommy.make("SpanType", text="labelA", project=self.project.item)
        label_b = mommy.make("SpanType", text="labelB", project=self.project.item)
        mommy.make("Span", example=self.example, start_offset=5, end_offset=10, user=self.user, label=label_a)
        mommy.make("Span", example=self.example, start_offset=10, end_offset=15, user=self.user, label=label_b)
        distribution = Span.objects.calc_label_distribution(
            examples=self.project.item.examples.all(), members=self.project.members, labels=SpanType.objects.all()
        )
        expected = {user.username: {label.text: 0 for label in SpanType.objects.all()} for user in self.project.members}
        expected[self.user.username][label_a.text] = 1
        expected[self.user.username][label_b.text] = 1
        self.assertEqual(distribution, expected)
