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
    def assert_records(self, repository, expected, confirmed_only=False):
        records = list(repository.list(export_approved=confirmed_only))
        self.assertEqual(len(records), len(expected))
        for record, expect in zip(records, expected):
            self.assertEqual(record.data, expect["data"])
            self.assertEqual(record.label, expect["label"])
            self.assertEqual(record.user, expect["user"])


class TestTextClassificationRepository(TestRepository):
    def prepare_data(self, project):
        self.confirmed_example = mommy.make("Example", project=project.item, text="confirmed")
        self.category1 = mommy.make("Category", example=self.confirmed_example, user=project.admin)
        self.category2 = mommy.make("Category", example=self.confirmed_example, user=project.annotator)
        mommy.make("ExampleState", example=self.confirmed_example, confirmed_by=project.admin)
        self.unconfirmed_example = mommy.make("Example", project=project.item, text="unconfirmed")

    def test_list(self):
        project = prepare_project(DOCUMENT_CLASSIFICATION)
        repository = TextClassificationRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [self.category1.label.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": [self.category2.label.text],
                "user": project.annotator.username,
            },
            {"data": self.unconfirmed_example.text, "label": [], "user": "unknown"},
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(DOCUMENT_CLASSIFICATION, collaborative_annotation=True)
        repository = TextClassificationRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [self.category1.label.text, self.category2.label.text],
                "user": "all",
            },
            {
                "data": self.unconfirmed_example.text,
                "label": [],
                "user": "all",
            },
        ]
        self.assert_records(repository, expected)

    def test_list_confirmed_example_only(self):
        project = prepare_project(DOCUMENT_CLASSIFICATION)
        repository = TextClassificationRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [self.category1.label.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": [self.category2.label.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected, confirmed_only=True)


class TestSeq2seqRepository(TestRepository):
    def prepare_data(self, project):
        self.confirmed_example = mommy.make("Example", project=project.item, text="confirmed")
        self.text1 = mommy.make("TextLabel", example=self.confirmed_example, user=project.admin)
        self.text2 = mommy.make("TextLabel", example=self.confirmed_example, user=project.annotator)
        mommy.make("ExampleState", example=self.confirmed_example, confirmed_by=project.admin)
        self.unconfirmed_example = mommy.make("Example", project=project.item, text="unconfirmed")

    def test_list(self):
        project = prepare_project(SEQ2SEQ)
        repository = Seq2seqRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [self.text1.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": [self.text2.text],
                "user": project.annotator.username,
            },
            {"data": self.unconfirmed_example.text, "label": [], "user": "unknown"},
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(SEQ2SEQ, collaborative_annotation=True)
        repository = Seq2seqRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [self.text1.text, self.text2.text],
                "user": "all",
            },
            {
                "data": self.unconfirmed_example.text,
                "label": [],
                "user": "all",
            },
        ]
        self.assert_records(repository, expected)

    def test_list_confirmed_example_only(self):
        project = prepare_project(SEQ2SEQ)
        repository = Seq2seqRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [self.text1.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": [self.text2.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected, confirmed_only=True)


class TestIntentDetectionSlotFillingRepository(TestRepository):
    def prepare_data(self, project):
        self.confirmed_example = mommy.make("Example", project=project.item, text="confirmed")
        self.category1 = mommy.make("Category", example=self.confirmed_example, user=project.admin)
        self.category2 = mommy.make("Category", example=self.confirmed_example, user=project.annotator)
        self.span = mommy.make("Span", example=self.confirmed_example, user=project.admin, start_offset=0, end_offset=1)
        mommy.make("ExampleState", example=self.confirmed_example, confirmed_by=project.admin)
        self.unconfirmed_example = mommy.make("Example", project=project.item, text="unconfirmed")

    def test_list(self):
        project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING)
        repository = IntentDetectionSlotFillingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": {
                    "cats": [self.category1.label.text],
                    "entities": [(self.span.start_offset, self.span.end_offset, self.span.label.text)],
                },
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": {
                    "cats": [self.category2.label.text],
                    "entities": [],
                },
                "user": project.annotator.username,
            },
            {"data": self.unconfirmed_example.text, "label": {"cats": [], "entities": []}, "user": "unknown"},
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING, collaborative_annotation=True)
        repository = IntentDetectionSlotFillingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": {
                    "cats": [self.category1.label.text, self.category2.label.text],
                    "entities": [(self.span.start_offset, self.span.end_offset, self.span.label.text)],
                },
                "user": "all",
            },
            {"data": self.unconfirmed_example.text, "label": {"cats": [], "entities": []}, "user": "all"},
        ]
        self.assert_records(repository, expected)

    def test_list_confirmed_example_only(self):
        project = prepare_project(INTENT_DETECTION_AND_SLOT_FILLING)
        repository = IntentDetectionSlotFillingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": {
                    "cats": [self.category1.label.text],
                    "entities": [(self.span.start_offset, self.span.end_offset, self.span.label.text)],
                },
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": {
                    "cats": [self.category2.label.text],
                    "entities": [],
                },
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected, confirmed_only=True)


class TestSequenceLabelingRepository(TestRepository):
    def prepare_data(self, project):
        self.confirmed_example = mommy.make("Example", project=project.item, text="confirmed")
        self.span1 = mommy.make(
            "Span", example=self.confirmed_example, user=project.admin, start_offset=0, end_offset=1
        )
        self.span2 = mommy.make(
            "Span", example=self.confirmed_example, user=project.annotator, start_offset=1, end_offset=2
        )
        mommy.make("ExampleState", example=self.confirmed_example, confirmed_by=project.admin)
        self.unconfirmed_example = mommy.make("Example", project=project.item, text="unconfirmed")

    def test_list(self):
        project = prepare_project(SEQUENCE_LABELING)
        repository = SequenceLabelingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [(self.span1.start_offset, self.span1.end_offset, self.span1.label.text)],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": [(self.span2.start_offset, self.span2.end_offset, self.span2.label.text)],
                "user": project.annotator.username,
            },
            {"data": self.unconfirmed_example.text, "label": [], "user": "unknown"},
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(SEQUENCE_LABELING, collaborative_annotation=True)
        repository = SequenceLabelingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [
                    (self.span1.start_offset, self.span1.end_offset, self.span1.label.text),
                    (self.span2.start_offset, self.span2.end_offset, self.span2.label.text),
                ],
                "user": "all",
            },
            {"data": self.unconfirmed_example.text, "label": [], "user": "all"},
        ]
        self.assert_records(repository, expected)

    def test_list_confirmed_example_only(self):
        project = prepare_project(SEQUENCE_LABELING)
        repository = SequenceLabelingRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.text,
                "label": [(self.span1.start_offset, self.span1.end_offset, self.span1.label.text)],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.text,
                "label": [(self.span2.start_offset, self.span2.end_offset, self.span2.label.text)],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected, confirmed_only=True)


class TestRelationExtractionRepository(TestRepository):
    def test_list(self):
        project = prepare_project(SEQUENCE_LABELING, use_relation=True)
        confirmed_example = mommy.make("Example", project=project.item, text="example")
        span1 = mommy.make("Span", example=confirmed_example, user=project.admin, start_offset=0, end_offset=1)
        span2 = mommy.make("Span", example=confirmed_example, user=project.admin, start_offset=1, end_offset=2)
        relation = mommy.make("Relation", from_id=span1, to_id=span2, example=confirmed_example, user=project.admin)
        mommy.make("ExampleState", example=confirmed_example, confirmed_by=project.admin)
        unconfirmed_example = mommy.make("Example", project=project.item, text="unconfirmed")
        repository = RelationExtractionRepository(project.item)
        expected = [
            {
                "data": confirmed_example.text,
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
            },
            {"data": unconfirmed_example.text, "label": {"entities": [], "relations": []}, "user": "unknown"},
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

    def test_list_confirmed_example_only(self):
        project = prepare_project(SEQUENCE_LABELING, use_relation=True)
        confirmed_example = mommy.make("Example", project=project.item, text="example")
        span1 = mommy.make("Span", example=confirmed_example, user=project.admin, start_offset=0, end_offset=1)
        span2 = mommy.make("Span", example=confirmed_example, user=project.admin, start_offset=1, end_offset=2)
        relation = mommy.make("Relation", from_id=span1, to_id=span2, example=confirmed_example, user=project.admin)
        mommy.make("ExampleState", example=confirmed_example, confirmed_by=project.admin)
        mommy.make("Example", project=project.item, text="unconfirmed")
        repository = RelationExtractionRepository(project.item)
        expected = [
            {
                "data": confirmed_example.text,
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
            },
        ]
        self.assert_records(repository, expected, confirmed_only=True)


class TestSpeech2TextRepository(TestRepository):
    def prepare_data(self, project):
        self.confirmed_example = mommy.make("Example", project=project.item)
        self.text1 = mommy.make("TextLabel", example=self.confirmed_example, user=project.admin)
        self.text2 = mommy.make("TextLabel", example=self.confirmed_example, user=project.annotator)
        mommy.make("ExampleState", example=self.confirmed_example, confirmed_by=project.admin)
        self.unconfirmed_example = mommy.make("Example", project=project.item, text="unconfirmed")

    def test_list(self):
        project = prepare_project(SPEECH2TEXT)
        repository = Speech2TextRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.text1.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.text2.text],
                "user": project.annotator.username,
            },
            {"data": self.unconfirmed_example.upload_name, "label": [], "user": "unknown"},
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(SPEECH2TEXT, collaborative_annotation=True)
        repository = Speech2TextRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.text1.text, self.text2.text],
                "user": "all",
            },
            {"data": self.unconfirmed_example.upload_name, "label": [], "user": "all"},
        ]
        self.assert_records(repository, expected)

    def test_list_confirmed_example_only(self):
        project = prepare_project(SPEECH2TEXT)
        repository = Speech2TextRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.text1.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.text2.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected, confirmed_only=True)


class TestFileRepository(TestRepository):
    def prepare_data(self, project):
        self.confirmed_example = mommy.make("Example", project=project.item, text="example")
        self.category1 = mommy.make("Category", example=self.confirmed_example, user=project.admin)
        self.category2 = mommy.make("Category", example=self.confirmed_example, user=project.annotator)
        mommy.make("ExampleState", example=self.confirmed_example, confirmed_by=project.admin)
        self.unconfirmed_example = mommy.make("Example", project=project.item, text="unconfirmed")

    def test_list(self):
        project = prepare_project(IMAGE_CLASSIFICATION)
        repository = FileRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.category1.label.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.category2.label.text],
                "user": project.annotator.username,
            },
            {"data": self.unconfirmed_example.upload_name, "label": [], "user": "unknown"},
        ]
        self.assert_records(repository, expected)

    def test_list_on_collaborative_annotation(self):
        project = prepare_project(IMAGE_CLASSIFICATION, collaborative_annotation=True)
        repository = FileRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.category1.label.text, self.category2.label.text],
                "user": "all",
            },
            {"data": self.unconfirmed_example.upload_name, "label": [], "user": "all"},
        ]
        self.assert_records(repository, expected)

    def test_list_confirmed_example_only(self):
        project = prepare_project(IMAGE_CLASSIFICATION)
        repository = FileRepository(project.item)
        self.prepare_data(project)
        expected = [
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.category1.label.text],
                "user": project.admin.username,
            },
            {
                "data": self.confirmed_example.upload_name,
                "label": [self.category2.label.text],
                "user": project.annotator.username,
            },
        ]
        self.assert_records(repository, expected, confirmed_only=True)
