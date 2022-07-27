from typing import Dict, List, Type

from django.db.models import QuerySet

from . import writers
from .catalog import CSV, JSON, JSONL, FastText
from .comments import Comments
from .formatters import (
    DictFormatter,
    FastTextCategoryFormatter,
    Formatter,
    JoinedCategoryFormatter,
    ListedCategoryFormatter,
    RenameFormatter,
    TupledSpanFormatter,
)
from .labels import BoundingBoxes, Categories, Labels, Relations, Segments, Spans, Texts
from data_export.models import DATA, ExportedExample
from projects.models import (
    BOUNDING_BOX,
    DOCUMENT_CLASSIFICATION,
    IMAGE_CAPTIONING,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEGMENTATION,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
    Project,
)


def create_writer(file_format: str) -> writers.Writer:
    mapping = {
        CSV.name: writers.CsvWriter(),
        JSON.name: writers.JsonWriter(),
        JSONL.name: writers.JsonlWriter(),
        FastText.name: writers.FastTextWriter(),
    }
    if file_format not in mapping:
        ValueError(f"Invalid format: {file_format}")
    return mapping[file_format]


def create_formatter(project: Project, file_format: str) -> List[Formatter]:
    use_relation = getattr(project, "use_relation", False)
    # text tasks
    mapper_text_classification = {DATA: "text", Categories.column: "label"}
    mapper_sequence_labeling = {DATA: "text", Spans.column: "label"}
    mapper_seq2seq = {DATA: "text", Texts.column: "label"}
    mapper_intent_detection = {DATA: "text", Categories.column: "cats"}
    mapper_relation_extraction = {DATA: "text"}

    # image tasks
    mapper_image_classification = {DATA: "filename", Categories.column: "label"}
    mapper_bounding_box = {DATA: "filename", BoundingBoxes.column: "bbox"}
    mapper_segmentation = {DATA: "filename", BoundingBoxes.column: "segmentation"}
    mapper_image_captioning = {DATA: "filename", Texts.column: "label"}

    # audio tasks
    mapper_speech2text = {DATA: "filename", Texts.column: "label"}

    mapping: Dict[str, Dict[str, List[Formatter]]] = {
        DOCUMENT_CLASSIFICATION: {
            CSV.name: [
                JoinedCategoryFormatter(Categories.column),
                JoinedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_text_classification),
            ],
            JSON.name: [
                ListedCategoryFormatter(Categories.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_text_classification),
            ],
            JSONL.name: [
                ListedCategoryFormatter(Categories.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_text_classification),
            ],
            FastText.name: [FastTextCategoryFormatter(Categories.column)],
        },
        SEQUENCE_LABELING: {
            JSONL.name: [
                DictFormatter(Spans.column),
                DictFormatter(Relations.column),
                DictFormatter(Comments.column),
                RenameFormatter(**mapper_relation_extraction),
            ]
            if use_relation
            else [
                TupledSpanFormatter(Spans.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_sequence_labeling),
            ]
        },
        SEQ2SEQ: {
            CSV.name: [
                JoinedCategoryFormatter(Texts.column),
                JoinedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_seq2seq),
            ],
            JSON.name: [
                ListedCategoryFormatter(Texts.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_seq2seq),
            ],
            JSONL.name: [
                ListedCategoryFormatter(Texts.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_seq2seq),
            ],
        },
        IMAGE_CLASSIFICATION: {
            JSONL.name: [
                ListedCategoryFormatter(Categories.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_image_classification),
            ],
        },
        SPEECH2TEXT: {
            JSONL.name: [
                ListedCategoryFormatter(Texts.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_speech2text),
            ],
        },
        INTENT_DETECTION_AND_SLOT_FILLING: {
            JSONL.name: [
                ListedCategoryFormatter(Categories.column),
                TupledSpanFormatter(Spans.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_intent_detection),
            ]
        },
        BOUNDING_BOX: {
            JSONL.name: [
                DictFormatter(BoundingBoxes.column),
                DictFormatter(Comments.column),
                RenameFormatter(**mapper_bounding_box),
            ]
        },
        SEGMENTATION: {
            JSONL.name: [
                DictFormatter(Segments.column),
                DictFormatter(Comments.column),
                RenameFormatter(**mapper_segmentation),
            ]
        },
        IMAGE_CAPTIONING: {
            JSONL.name: [
                ListedCategoryFormatter(Texts.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_image_captioning),
            ]
        },
    }
    return mapping[project.project_type][file_format]


def select_label_collection(project: Project) -> List[Type[Labels]]:
    use_relation = getattr(project, "use_relation", False)
    mapping: Dict[str, List[Type[Labels]]] = {
        DOCUMENT_CLASSIFICATION: [Categories],
        SEQUENCE_LABELING: [Spans, Relations] if use_relation else [Spans],
        SEQ2SEQ: [Texts],
        IMAGE_CLASSIFICATION: [Categories],
        SPEECH2TEXT: [Texts],
        INTENT_DETECTION_AND_SLOT_FILLING: [Categories, Spans],
        BOUNDING_BOX: [BoundingBoxes],
        SEGMENTATION: [Segments],
        IMAGE_CAPTIONING: [Texts],
    }
    return mapping[project.project_type]


def create_labels(project: Project, examples: QuerySet[ExportedExample], user=None) -> List[Labels]:
    label_collections = select_label_collection(project)
    labels = [label_collection(examples=examples, user=user) for label_collection in label_collections]
    return labels


def create_comment(examples: QuerySet[ExportedExample], user=None) -> List[Comments]:
    return [Comments(examples=examples, user=user)]
