import unittest

from model_mommy import mommy

from ..pipeline.repositories import (
    FileRepository,
    IntentDetectionSlotFillingRepository,
    RelationExtractionRepository,
    Seq2seqRepository,
    SequenceLabelingRepository,
    Speech2TextRepository,
    TextClassificationRepository,
)
from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
)
from projects.tests.utils import prepare_project


class TestRepository(unittest.TestCase):
    def assert_records(self, repository, expected):
        records = list(repository.list())
        self.assertEqual(len(records), len(expected))
        for record, expect in zip(records, expected):
            self.assertEqual(record.data, expect["data"])
            self.assertEqual(record.label, expect["label"])
            self.assertEqual(record.user, expect["user"])


class TestTextClassificationRepository(TestRepository):
    def prepare_data(self, project):
        self.example = mommy.make("Example", project=project.item, text="example")
        self.category1 = mommy.make("Category", example=self.example, user=project.admin)
        self.category2 = mommy.make("Category", example=self.example, user=project.annotator)

    def test_list(self):
        project = prepare_project(DOCUMENT_CLASSIFICATION)
        repository = TextClassificationRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": [self.category1.label.text],
                "user": project.admin.username,
            },
            {
                "data": self.example.text,
                "label": [self.category2.label.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(DOCUMENT_CLASSIFICATION, collaborative_annotation=True)
        repository = TextClassificationRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": [self.category1.label.text, self.category2.label.text],
                "user": "all",
            }
        ]
        self.assert_records(repository, expected)


class TestSeq2seqRepository(TestRepository):
    def prepare_data(self, project):
        self.example = mommy.make("Example", project=project.item, text="example")
        self.text1 = mommy.make("TextLabel", example=self.example, user=project.admin)
        self.text2 = mommy.make("TextLabel", example=self.example, user=project.annotator)

    def test_list(self):
        project = prepare_project(SEQ2SEQ)
        repository = Seq2seqRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": [self.text1.text],
                "user": project.admin.username,
            },
            {
                "data": self.example.text,
                "label": [self.text2.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(SEQ2SEQ, collaborative_annotation=True)
        repository = Seq2seqRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": [self.text1.text, self.text2.text],
                "user": "all",
            }
        ]
        self.assert_records(repository, expected)


class TestIntentDetectionSlotFillingRepository(TestRepository):
    def prepare_data(self, project):
        self.example = mommy.make("Example", project=project.item, text="example")
        self.category1 = mommy.make("Category", example=self.example, user=project.admin)
        self.category2 = mommy.make("Category", example=self.example, user=project.annotator)
        self.span = mommy.make("Span", example=self.example, user=project.admin, start_offset=0, end_offset=1)

    def test_list(self):
        project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING)
        repository = IntentDetectionSlotFillingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": {
                    "cats": [self.category1.label.text],
                    "entities": [(self.span.start_offset, self.span.end_offset, self.span.label.text)],
                },
                "user": project.admin.username,
            },
            {
                "data": self.example.text,
                "label": {
                    "cats": [self.category2.label.text],
                    "entities": [],
                },
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING, collaborative_annotation=True)
        repository = IntentDetectionSlotFillingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": {
                    "cats": [self.category1.label.text, self.category2.label.text],
                    "entities": [(self.span.start_offset, self.span.end_offset, self.span.label.text)],
                },
                "user": "all",
            }
        ]
        self.assert_records(repository, expected)


class TestSequenceLabelingRepository(TestRepository):
    def prepare_data(self, project):
        self.example = mommy.make("Example", project=project.item, text="example")
        self.span1 = mommy.make("Span", example=self.example, user=project.admin, start_offset=0, end_offset=1)
        self.span2 = mommy.make("Span", example=self.example, user=project.annotator, start_offset=1, end_offset=2)

    def test_list(self):
        project = prepare_project(SEQUENCE_LABELING)
        repository = SequenceLabelingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": [(self.span1.start_offset, self.span1.end_offset, self.span1.label.text)],
                "user": project.admin.username,
            },
            {
                "data": self.example.text,
                "label": [(self.span2.start_offset, self.span2.end_offset, self.span2.label.text)],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(SEQUENCE_LABELING, collaborative_annotation=True)
        repository = SequenceLabelingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.text,
                "label": [
                    (self.span1.start_offset, self.span1.end_offset, self.span1.label.text),
                    (self.span2.start_offset, self.span2.end_offset, self.span2.label.text),
                ],
                "user": "all",
            }
        ]
        self.assert_records(repository, expected)


class TestRelationExtractionRepository(TestRepository):
    def test_list(self):
        project = prepare_project(SEQUENCE_LABELING, use_relation=True)
        example = mommy.make("Example", project=project.item, text="example")
        span1 = mommy.make("Span", example=example, user=project.admin, start_offset=0, end_offset=1)
        span2 = mommy.make("Span", example=example, user=project.admin, start_offset=1, end_offset=2)
        relation = mommy.make("Relation", from_id=span1, to_id=span2, example=example, user=project.admin)
        repository = RelationExtractionRepository(project.item)
        expected = [
            {
                "data": example.text,
                "label": {
                    "entities": [
                        {
                            "id": span1.id,
                            "start_offset": span1.start_offset,
                            "end_offset": span1.end_offset,
                            "label": span1.label.text,
                        },
                        {
                            "id": span2.id,
                            "start_offset": span2.start_offset,
                            "end_offset": span2.end_offset,
                            "label": span2.label.text,
                        },
                    ],
                    "relations": [
                        {"id": relation.id, "from_id": span1.id, "to_id": span2.id, "type": relation.type.text}
                    ],
                },
                "user": project.admin.username,
            }
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(SEQUENCE_LABELING, collaborative_annotation=True, use_relation=True)
        example = mommy.make("Example", project=project.item, text="example")
        span1 = mommy.make("Span", example=example, user=project.admin, start_offset=0, end_offset=1)
        span2 = mommy.make("Span", example=example, user=project.annotator, start_offset=1, end_offset=2)
        relation = mommy.make("Relation", from_id=span1, to_id=span2, example=example, user=project.admin)
        repository = RelationExtractionRepository(project.item)
        expected = [
            {
                "data": example.text,
                "label": {
                    "entities": [
                        {
                            "id": span1.id,
                            "start_offset": span1.start_offset,
                            "end_offset": span1.end_offset,
                            "label": span1.label.text,
                        },
                        {
                            "id": span2.id,
                            "start_offset": span2.start_offset,
                            "end_offset": span2.end_offset,
                            "label": span2.label.text,
                        },
                    ],
                    "relations": [
                        {"id": relation.id, "from_id": span1.id, "to_id": span2.id, "type": relation.type.text}
                    ],
                },
                "user": "all",
            }
        ]
        self.assert_records(repository, expected)


class TestSpeech2TextRepository(TestRepository):
    def prepare_data(self, project):
        self.example = mommy.make("Example", project=project.item, text="example")
        self.text1 = mommy.make("TextLabel", example=self.example, user=project.admin)
        self.text2 = mommy.make("TextLabel", example=self.example, user=project.annotator)

    def test_list(self):
        project = prepare_project(SPEECH2TEXT)
        repository = Speech2TextRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.filename,
                "label": [self.text1.text],
                "user": project.admin.username,
            },
            {
                "data": self.example.filename,
                "label": [self.text2.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(SPEECH2TEXT, collaborative_annotation=True)
        repository = Speech2TextRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.filename,
                "label": [self.text1.text, self.text2.text],
                "user": "all",
            }
        ]
        self.assert_records(repository, expected)


class TestFileRepository(TestRepository):
    def prepare_data(self, project):
        self.example = mommy.make("Example", project=project.item, text="example")
        self.category1 = mommy.make("Category", example=self.example, user=project.admin)
        self.category2 = mommy.make("Category", example=self.example, user=project.annotator)

    def test_list(self):
        project = prepare_project(IMAGE_CLASSIFICATION)
        repository = FileRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.filename,
                "label": [self.category1.label.text],
                "user": project.admin.username,
            },
            {
                "data": self.example.filename,
                "label": [self.category2.label.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(IMAGE_CLASSIFICATION, collaborative_annotation=True)
        repository = FileRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.example.filename,
                "label": [self.category1.label.text, self.category2.label.text],
                "user": "all",
            }
        ]
        self.assert_records(repository, expected)
