from typing import Type

from ...models import (DOCUMENT_CLASSIFICATION, DOCUMENT_SIMILARITY, IMAGE_CLASSIFICATION, SEQ2SEQ,
                       SEQUENCE_LABELING, SPEECH2TEXT)
from . import catalog, repositories, writer


def create_repository(project) -> repositories.BaseRepository:
    mapping = {
        DOCUMENT_CLASSIFICATION: repositories.TextClassificationRepository,
        DOCUMENT_SIMILARITY: repositories.TextSimilarityRepository,
        SEQUENCE_LABELING: repositories.SequenceLabelingRepository,
        SEQ2SEQ: repositories.Seq2seqRepository,
        IMAGE_CLASSIFICATION: repositories.FileRepository,
        SPEECH2TEXT: repositories.Speech2TextRepository,
    }
    if project.project_type not in mapping:
        ValueError(f'Invalid project type: {project.project_type}')
    repository = mapping.get(project.project_type)(project)
    return repository


def create_writer(format: str) -> Type[writer.BaseWriter]:
    mapping = {
        catalog.CSV.name: writer.CsvWriter,
        catalog.JSON.name: writer.JSONWriter,
        catalog.JSONL.name: writer.JSONLWriter,
        catalog.FastText.name: writer.FastTextWriter,
    }
    if format not in mapping:
        ValueError(f'Invalid format: {format}')
    return mapping[format]
