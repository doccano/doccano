from ...models import (DOCUMENT_CLASSIFICATION, IMAGE_CLASSIFICATION, SEQ2SEQ,
                       SEQUENCE_LABELING)
from . import catalog, data, dataset, label


def get_data_class(project_type: str):
    text_projects = [DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ]
    if project_type in text_projects:
        return data.TextData
    else:
        return data.FileData


def get_dataset_class(format: str):
    mapping = {
        catalog.TextFile.name: dataset.TextFileDataset,
        catalog.TextLine.name: dataset.TextLineDataset,
        catalog.CSV.name: dataset.CsvDataset,
        catalog.JSONL.name: dataset.JSONLDataset,
        catalog.JSON.name: dataset.JSONDataset,
        catalog.FastText.name: dataset.FastTextDataset,
        catalog.Excel.name: dataset.ExcelDataset,
        catalog.CoNLL.name: dataset.CoNLLDataset,
        catalog.ImageFile.name: dataset.FileBaseDataset,
    }
    if format not in mapping:
        ValueError(f'Invalid format: {format}')
    return mapping[format]


def get_label_class(project_type: str):
    mapping = {
        DOCUMENT_CLASSIFICATION: label.CategoryLabel,
        SEQUENCE_LABELING: label.OffsetLabel,
        SEQ2SEQ: label.TextLabel,
        IMAGE_CLASSIFICATION: label.CategoryLabel,
    }
    if project_type not in mapping:
        ValueError(f'Invalid project type: {project_type}')
    return mapping[project_type]
