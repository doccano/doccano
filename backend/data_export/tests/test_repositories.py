import unittest

from model_mommy import mommy

from projects.models import INTENT_DETECTION_AND_SLOT_FILLING
from projects.tests.utils import prepare_project
from ..pipeline.repositories import IntentDetectionSlotFillingRepository


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
