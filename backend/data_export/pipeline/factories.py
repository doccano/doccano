from typing import Type

from django.db.models import QuerySet

from . import catalog, formatters, labels, repositories, writers
from .labels import Labels
from examples.models import Example
from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
)


def create_repository(project, file_format: str):
    if getattr(project, "use_relation", False) and file_format == catalog.JSONLRelation.name:
        return repositories.RelationExtractionRepository(project)
    mapping = {
        DOCUMENT_CLASSIFICATION: repositories.TextClassificationRepository,
        SEQUENCE_LABELING: repositories.SequenceLabelingRepository,
        SEQ2SEQ: repositories.Seq2seqRepository,
        IMAGE_CLASSIFICATION: repositories.FileRepository,
        SPEECH2TEXT: repositories.Speech2TextRepository,
        INTENT_DETECTION_AND_SLOT_FILLING: repositories.IntentDetectionSlotFillingRepository,
    }
    if project.project_type not in mapping:
        ValueError(f"Invalid project type: {project.project_type}")
    repository = mapping[project.project_type](project)
    return repository


def create_writer(file_format: str) -> writers.Writer:
    mapping = {
        catalog.CSV.name: writers.CsvWriter,
        catalog.JSON.name: writers.JsonWriter,
        catalog.JSONL.name: writers.JsonlWriter,
        # catalog.FastText.name: writers.FastTextWriter,
    }
    if file_format not in mapping:
        ValueError(f"Invalid format: {file_format}")
    return mapping[file_format]()


def create_formatter(project, file_format: str):
    mapping = {
        DOCUMENT_CLASSIFICATION: {
            catalog.CSV.name: formatters.JoinedCategoryFormatter,
            catalog.JSON.name: formatters.ListedCategoryFormatter,
            catalog.JSONL.name: formatters.ListedCategoryFormatter,
        },
        SEQUENCE_LABELING: {},
        SEQ2SEQ: {},
        IMAGE_CLASSIFICATION: {},
        SPEECH2TEXT: {},
        INTENT_DETECTION_AND_SLOT_FILLING: {},
    }
    return mapping[project.project_type][file_format]


def select_label_collection(project):
    mapping = {DOCUMENT_CLASSIFICATION: labels.Categories}
    return mapping[project.project_type]


def create_labels(label_collection_class: Type[Labels], examples: QuerySet[Example], user=None):
    return label_collection_class(examples, user)
