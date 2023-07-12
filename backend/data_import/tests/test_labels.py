import uuid
from unittest.mock import MagicMock

from django.test import TestCase
from model_mommy import mommy

from data_import.models import DummyLabelType
from data_import.pipeline.label import (
    CategoryLabel,
    RelationLabel,
    SpanLabel,
    TextLabel,
)
from data_import.pipeline.label_types import LabelTypes
from data_import.pipeline.labels import Categories, Relations, Spans, Texts
from label_types.models import CategoryType, RelationType, SpanType
from labels.models import Category, Relation, Span
from labels.models import TextLabel as TextLabelModel
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestCategories(TestCase):
    def setUp(self):
        self.types = LabelTypes(CategoryType)
        self.project = prepare_project(ProjectType.DOCUMENT_CLASSIFICATION)
        self.user = self.project.admin
        example_uuid = uuid.uuid4()
        labels = [
            CategoryLabel(example_uuid=example_uuid, label="A"),
            CategoryLabel(example_uuid=example_uuid, label="B"),
        ]
        example = mommy.make("Example", project=self.project.item, uuid=example_uuid)
        self.examples = MagicMock()
        self.examples.__getitem__.return_value = example
        self.examples.__contains__.return_value = True
        self.categories = Categories(labels, self.types)

    def test_clean(self):
        self.categories.clean(self.project.item)
        self.assertEqual(len(self.categories), 2)

    def test_clean_with_exclusive_labels(self):
        self.project.item.single_class_classification = True
        self.project.item.save()
        self.categories.clean(self.project.item)
        self.assertEqual(len(self.categories), 1)

    def test_save(self):
        self.categories.save_types(self.project.item)
        self.categories.save(self.user, self.examples)
        self.assertEqual(Category.objects.count(), 2)

    def test_save_types(self):
        self.categories.save_types(self.project.item)
        self.assertEqual(CategoryType.objects.count(), 2)


class TestSpans(TestCase):
    def setUp(self):
        self.types = LabelTypes(SpanType)
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING, allow_overlapping=True)
        self.user = self.project.admin
        example_uuid = uuid.uuid4()
        labels = [
            SpanLabel(example_uuid=example_uuid, label="A", start_offset=0, end_offset=1),
            SpanLabel(example_uuid=example_uuid, label="B", start_offset=0, end_offset=3),
            SpanLabel(example_uuid=example_uuid, label="B", start_offset=3, end_offset=4),
        ]
        example = mommy.make("Example", project=self.project.item, uuid=example_uuid)
        self.examples = MagicMock()
        self.examples.__getitem__.return_value = example
        self.examples.__contains__.return_value = True
        self.spans = Spans(labels, self.types)

    def disable_overlapping(self):
        self.project.item.allow_overlapping = False
        self.project.item.save()

    def test_clean(self):
        self.disable_overlapping()
        self.spans.clean(self.project.item)
        self.assertEqual(len(self.spans), 2)

    def test_clean_with_overlapping(self):
        self.spans.clean(self.project.item)
        self.assertEqual(len(self.spans), 3)

    def test_clean_with_multiple_examples(self):
        self.disable_overlapping()
        example_uuid1 = uuid.uuid4()
        example_uuid2 = uuid.uuid4()
        labels = [
            SpanLabel(example_uuid=example_uuid1, label="A", start_offset=0, end_offset=1),
            SpanLabel(example_uuid=example_uuid2, label="B", start_offset=0, end_offset=3),
        ]
        mommy.make("Example", project=self.project.item, uuid=example_uuid1)
        mommy.make("Example", project=self.project.item, uuid=example_uuid2)
        spans = Spans(labels, self.types)
        spans.clean(self.project.item)
        self.assertEqual(len(spans), 2)

    def test_save(self):
        self.spans.save_types(self.project.item)
        self.spans.save(self.user, self.examples)
        self.assertEqual(Span.objects.count(), 3)

    def test_save_types(self):
        self.spans.save_types(self.project.item)
        self.assertEqual(SpanType.objects.count(), 2)


class TestTexts(TestCase):
    def setUp(self):
        self.types = LabelTypes(DummyLabelType)
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING)
        self.user = self.project.admin
        example_uuid = uuid.uuid4()
        labels = [
            TextLabel(example_uuid=example_uuid, text="A"),
            TextLabel(example_uuid=example_uuid, text="B"),
        ]
        example = mommy.make("Example", project=self.project.item, uuid=example_uuid)
        self.examples = MagicMock()
        self.examples.__getitem__.return_value = example
        self.examples.__contains__.return_value = True
        self.texts = Texts(labels, self.types)

    def test_clean(self):
        self.texts.clean(self.project.item)
        self.assertEqual(len(self.texts), 2)

    def test_save(self):
        self.texts.save_types(self.project.item)
        self.texts.save(self.user, self.examples)
        self.assertEqual(TextLabelModel.objects.count(), 2)

    def test_save_types(self):
        # nothing happen
        self.texts.save_types(self.project.item)


class TestRelations(TestCase):
    def setUp(self):
        self.types = LabelTypes(RelationType)
        self.project = prepare_project(ProjectType.SEQUENCE_LABELING, use_relation=True)
        self.user = self.project.admin
        example_uuid = uuid.uuid4()
        example = mommy.make("Example", project=self.project.item, uuid=example_uuid, text="hello world")
        from_span = mommy.make("Span", example=example, start_offset=0, end_offset=1)
        to_span = mommy.make("Span", example=example, start_offset=2, end_offset=3)
        labels = [
            RelationLabel(example_uuid=example_uuid, type="A", from_id=from_span.id, to_id=to_span.id),
        ]
        self.relations = Relations(labels, self.types)
        self.spans = MagicMock()
        self.spans.id_to_span = {(from_span.id, str(example_uuid)): from_span, (to_span.id, str(example_uuid)): to_span}
        self.examples = MagicMock()
        self.examples.__getitem__.return_value = example
        self.examples.__contains__.return_value = True

    def test_clean(self):
        self.relations.clean(self.project.item)
        self.assertEqual(len(self.relations), 1)

    def test_save(self):
        self.relations.save_types(self.project.item)
        self.relations.save(self.user, self.examples, spans=self.spans)
        self.assertEqual(Relation.objects.count(), 1)

    def test_save_types(self):
        self.relations.save_types(self.project.item)
        self.assertEqual(RelationType.objects.count(), 1)
