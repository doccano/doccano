import abc

from django.test import TestCase
from model_mommy import mommy

from api.models import SEQUENCE_LABELING, Span

from .api.utils import prepare_project


class TestSpanAnnotation(abc.ABC, TestCase):
    overlapping = False
    collaborative = False

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(
            SEQUENCE_LABELING,
            allow_overlapping=cls.overlapping,
            collaborative_annotation=cls.collaborative
        )
        cls.example = mommy.make('Example', project=cls.project.item)
        cls.label_type = mommy.make('SpanType', project=cls.project.item)
        users = cls.project.users
        cls.user = users[0]
        cls.another_user = users[1]
        cls.span = Span(
            example=cls.example,
            label=cls.label_type,
            user=cls.user,
            start_offset=0,
            end_offset=5
        )

    def test_can_annotate_span_to_unannotated_data(self):
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)


class NonCollaborativeMixin:

    def test_allow_another_user_to_annotate_same_span(self):
        mommy.make(
            'Span',
            example=self.example,
            label=self.label_type,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)


class TestNonOverlappingSpanAnnotation(TestSpanAnnotation, NonCollaborativeMixin):
    overlapping = False
    collaborative = False

    def test_cannot_annotate_same_span_to_annotated_data(self):
        mommy.make(
            'Span',
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
            'Span',
            example=self.example,
            user=self.user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertFalse(can_annotate)


class TestOverlappingSpanAnnotation(TestSpanAnnotation, NonCollaborativeMixin):
    overlapping = True
    collaborative = False

    def test_can_annotate_same_span_to_annotated_data(self):
        mommy.make(
            'Span',
            example=self.example,
            label=self.label_type,
            user=self.user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset,
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)


class TestCollaborativeNonOverlappingSpanAnnotation(TestSpanAnnotation):
    overlapping = False
    collaborative = True

    def test_deny_another_user_to_annotate_same_span_type(self):
        mommy.make(
            'Span',
            example=self.example,
            label=self.label_type,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertFalse(can_annotate)

    def test_deny_another_user_to_annotate_different_span_type(self):
        mommy.make(
            'Span',
            example=self.example,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertFalse(can_annotate)


class TestCollaborativeOverlappingSpanAnnotation(TestSpanAnnotation):
    overlapping = True
    collaborative = True

    def test_allow_another_user_to_annotate_same_span(self):
        mommy.make(
            'Span',
            example=self.example,
            label=self.label_type,
            user=self.another_user,
            start_offset=self.span.start_offset,
            end_offset=self.span.end_offset
        )
        can_annotate = Span.objects.can_annotate(self.span, self.project.item)
        self.assertTrue(can_annotate)
