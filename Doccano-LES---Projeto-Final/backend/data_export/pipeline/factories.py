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
from projects.models import Project, ProjectType


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
        ProjectType.DOCUMENT_CLASSIFICATION: {
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
        ProjectType.SEQUENCE_LABELING: {
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
        ProjectType.SEQ2SEQ: {
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
        ProjectType.IMAGE_CLASSIFICATION: {
            JSONL.name: [
                ListedCategoryFormatter(Categories.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_image_classification),
            ],
        },
        ProjectType.SPEECH2TEXT: {
            JSONL.name: [
                ListedCategoryFormatter(Texts.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_speech2text),
            ],
        },
        ProjectType.INTENT_DETECTION_AND_SLOT_FILLING: {
            JSONL.name: [
                ListedCategoryFormatter(Categories.column),
                TupledSpanFormatter(Spans.column),
                ListedCategoryFormatter(Comments.column),
                RenameFormatter(**mapper_intent_detection),
            ]
        },
        ProjectType.BOUNDING_BOX: {
            JSONL.name: [
                DictFormatter(BoundingBoxes.column),
                DictFormatter(Comments.column),
                RenameFormatter(**mapper_bounding_box),
            ]
        },
        ProjectType.SEGMENTATION: {
            JSONL.name: [
                DictFormatter(Segments.column),
                DictFormatter(Comments.column),
                RenameFormatter(**mapper_segmentation),
            ]
        },
        ProjectType.IMAGE_CAPTIONING: {
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
        ProjectType.DOCUMENT_CLASSIFICATION: [Categories],
        ProjectType.SEQUENCE_LABELING: [Spans, Relations] if use_relation else [Spans],
        ProjectType.SEQ2SEQ: [Texts],
        ProjectType.IMAGE_CLASSIFICATION: [Categories],
        ProjectType.SPEECH2TEXT: [Texts],
        ProjectType.INTENT_DETECTION_AND_SLOT_FILLING: [Categories, Spans],
        ProjectType.BOUNDING_BOX: [BoundingBoxes],
        ProjectType.SEGMENTATION: [Segments],
        ProjectType.IMAGE_CAPTIONING: [Texts],
    }
    return mapping[project.project_type]


def create_labels(project: Project, examples: QuerySet[ExportedExample], user=None) -> List[Labels]:
    label_collections = select_label_collection(project)
    labels = [label_collection(examples=examples, user=user) for label_collection in label_collections]
    return labels


def create_comment(examples: QuerySet[ExportedExample], user=None) -> List[Comments]:
    return [Comments(examples=examples, user=user)]
