from typing import Dict, List, Type

from django.db.models import QuerySet

from . import catalog, formatters, labels, writers
from .labels import Labels
from data_export.models import ExportedExample
from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
    Project,
)


def create_writer(file_format: str) -> writers.Writer:
    mapping = {
        catalog.CSV.name: writers.CsvWriter(),
        catalog.JSON.name: writers.JsonWriter(),
        catalog.JSONL.name: writers.JsonlWriter(),
        catalog.FastText.name: writers.FastTextWriter(),
    }
    if file_format not in mapping:
        ValueError(f"Invalid format: {file_format}")
    return mapping[file_format]


def create_formatter(project: Project, file_format: str) -> List[formatters.Formatter]:
    use_relation = getattr(project, "use_relation", False)
    mapping: Dict[str, Dict[str, List[formatters.Formatter]]] = {
        DOCUMENT_CLASSIFICATION: {
            catalog.CSV.name: [formatters.JoinedCategoryFormatter(labels.Categories.column)],
            catalog.JSON.name: [formatters.ListedCategoryFormatter(labels.Categories.column)],
            catalog.JSONL.name: [formatters.ListedCategoryFormatter(labels.Categories.column)],
            catalog.FastText.name: [formatters.FastTextCategoryFormatter(labels.Categories.column)],
        },
        SEQUENCE_LABELING: {
            catalog.JSONL.name: [
                formatters.DictFormatter(labels.Spans.column),
                formatters.DictFormatter(labels.Relations.column),
            ]
            if use_relation
            else [formatters.TupledSpanFormatter(labels.Spans.column)]
        },
        SEQ2SEQ: {
            catalog.CSV.name: [formatters.JoinedCategoryFormatter(labels.Texts.column)],
            catalog.JSON.name: [formatters.ListedCategoryFormatter(labels.Texts.column)],
            catalog.JSONL.name: [formatters.ListedCategoryFormatter(labels.Texts.column)],
        },
        IMAGE_CLASSIFICATION: {
            catalog.JSONL.name: [formatters.ListedCategoryFormatter(labels.Categories.column)],
        },
        SPEECH2TEXT: {
            catalog.JSONL.name: [formatters.ListedCategoryFormatter(labels.Texts.column)],
        },
        INTENT_DETECTION_AND_SLOT_FILLING: {
            catalog.JSONL.name: [
                formatters.ListedCategoryFormatter(labels.Categories.column),
                formatters.TupledSpanFormatter(labels.Spans.column),
            ]
        },
    }
    return mapping[project.project_type][file_format]


def select_label_collection(project: Project) -> List[Type[Labels]]:
    use_relation = getattr(project, "use_relation", False)
    mapping: Dict[str, List[Type[Labels]]] = {
        DOCUMENT_CLASSIFICATION: [labels.Categories],
        SEQUENCE_LABELING: [labels.Spans, labels.Relations] if use_relation else [labels.Spans],
        SEQ2SEQ: [labels.Texts],
        IMAGE_CLASSIFICATION: [labels.Categories],
        SPEECH2TEXT: [labels.Texts],
        INTENT_DETECTION_AND_SLOT_FILLING: [labels.Categories, labels.Spans],
    }
    return mapping[project.project_type]


def create_labels(project: Project, examples: QuerySet[ExportedExample], user=None) -> List[Labels]:
    label_collections = select_label_collection(project)
    labels = [label_collection(examples=examples, user=user) for label_collection in label_collections]
    return labels
