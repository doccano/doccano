from ...models import DOCUMENT_CLASSIFICATION, SEQ2SEQ, SEQUENCE_LABELING
from . import repositories


def create_repository(project) -> repositories.BaseRepository:
    mapping = {
        DOCUMENT_CLASSIFICATION: repositories.TextClassificationRepository,
        SEQUENCE_LABELING: repositories.SequenceLabelingRepository,
        SEQ2SEQ: repositories.Seq2seqRepository,
    }
    if project.project_type not in mapping:
        ValueError(f'Invalid project type: {project.project_type}')
    repository = mapping.get(project.project_type)(project)
    return repository
