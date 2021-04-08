from . import data, dataset, label, catalog
from ...models import DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ


def get_data_class(project_type: str):
    text_projects = [DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ]
    if project_type in text_projects:
        return data.TextData
    else:
        return data.FileData


def get_dataset_class(format: str):
    if format == catalog.CSV:
        return dataset.CsvDataset
    elif format == catalog.JSONL:
        return dataset.JSONLDataset
    elif format == catalog.JSONL:
        return dataset.JSONDataset
    elif format == catalog.FastText:
        return dataset.FastTextDataset
    elif format == catalog.EXCEL:
        return dataset.ExcelDataset
    else:
        ValueError(f'Invalid format: {format}')


def get_label_class(project_type: str):
    if project_type == DOCUMENT_CLASSIFICATION:
        return label.CategoryLabel
    elif project_type == SEQUENCE_LABELING:
        return label.OffsetLabel
    elif project_type == SEQ2SEQ:
        return label.TextLabel
    else:
        ValueError(f'Invalid project type: {project_type}')
