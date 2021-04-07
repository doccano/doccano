from . import dataset
from . import label


def get_dataset_class(format: str):
    if format == 'csv':
        return dataset.CsvDataset
    elif format == 'jsonl':
        return dataset.JSONLDataset
    elif format == 'json':
        return dataset.JSONDataset
    elif format == 'fasttext':
        return dataset.FastTextDataset
    elif format == 'excel':
        return dataset.ExcelDataset
    else:
        ValueError(f'Invalid format: {format}')


def get_label_class(project_type: str):
    if project_type == 'DocumentClassification':
        return label.CategoryLabel
    elif project_type == 'SequenceLabeling':
        return label.OffsetLabel
    elif project_type == 'Seq2seq':
        return label.TextLabel
    else:
        ValueError(f'Invalid project type: {project_type}')
