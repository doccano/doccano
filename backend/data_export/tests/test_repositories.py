import unittest

from model_mommy import mommy

from ..pipeline.repositories import (
    IntentDetectionSlotFillingRepository,
    RelationExtractionRepository,
)
from projects.models import INTENT_DETECTION_AND_SLOT_FILLING, SEQUENCE_LABELING
from projects.tests.utils import prepare_project


class TestCSVWriter(unittest.TestCase):
    def setUp(self):
        self.project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING)

    def test_list(self):
        example = mommy.make("Example", project=self.project.item, text="example")
        category = mommy.make("Category", example=example, user=self.project.admin)
        span = mommy.make("Span", example=example, user=self.project.admin, start_offset=0, end_offset=1)
        repository = IntentDetectionSlotFillingRepository(self.project.item)
        expected = [
            {
                "data": example.text,
                "label": {
                    "cats": [category.label.text],
                    "entities": [(span.start_offset, span.end_offset, span.label.text)],
                },
            }
        ]
        records = list(repository.list())
        self.assertEqual(len(records), len(expected))
        for record, expect in zip(records, expected):
            self.assertEqual(record.data, expect["data"])
            self.assertEqual(record.label["cats"], expect["label"]["cats"])
            self.assertEqual(record.label["entities"], expect["label"]["entities"])


class TestRelationExtractionRepository(unittest.TestCase):
    def setUp(self):
        self.project = prepare_project(SEQUENCE_LABELING, use_relation=True)

    def test_label_per_user(self):
        from_entity = mommy.make("Span", start_offset=0, end_offset=1, user=self.project.admin)
        to_entity = mommy.make(
            "Span", start_offset=1, end_offset=2, example=from_entity.example, user=self.project.admin
        )
        relation = mommy.make(
            "Relation", from_id=from_entity, to_id=to_entity, example=from_entity.example, user=self.project.admin
        )
        repository = RelationExtractionRepository(self.project.item)
        expected = {
            "admin": {
                "entities": [
                    {
                        "id": from_entity.id,
                        "start_offset": from_entity.start_offset,
                        "end_offset": from_entity.end_offset,
                        "label": from_entity.label.text,
                    },
                    {
                        "id": to_entity.id,
                        "start_offset": to_entity.start_offset,
                        "end_offset": to_entity.end_offset,
                        "label": to_entity.label.text,
                    },
                ],
                "relations": [
                    {"id": relation.id, "from_id": from_entity.id, "to_id": to_entity.id, "type": relation.type.text}
                ],
            }
        }
        actual = repository.label_per_user(from_entity.example)
        self.assertDictEqual(actual, expected)
