from typing import List

from . import (
    builders,
    catalog,
    cleaners,
    data,
    labeled_examples,
    labels,
    parsers,
    readers,
)
from .formatters import DataFormatter, LabelFormatter
from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
    Project,
)


def get_data_class(project_type: str):
    text_projects = [DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ, INTENT_DETECTION_AND_SLOT_FILLING]
    if project_type in text_projects:
        return data.TextData
    else:
        return data.BinaryData


def create_parser(file_format: str, **kwargs):
    mapping = {
        catalog.TextFile.name: parsers.TextFileParser,
        catalog.TextLine.name: parsers.LineParser,
        catalog.CSV.name: parsers.CSVParser,
        catalog.JSONL.name: parsers.JSONLParser,
        catalog.JSON.name: parsers.JSONParser,
        catalog.FastText.name: parsers.FastTextParser,
        catalog.Excel.name: parsers.ExcelParser,
        catalog.CoNLL.name: parsers.CoNLLParser,
        catalog.ImageFile.name: parsers.PlainParser,
        catalog.AudioFile.name: parsers.PlainParser,
    }
    if file_format not in mapping:
        raise ValueError(f"Invalid format: {file_format}")
    return mapping[file_format](**kwargs)


def get_label_class(project_type: str):
    mapping = {
        DOCUMENT_CLASSIFICATION: labels.CategoryLabel,
        SEQUENCE_LABELING: labels.SpanLabel,
        SEQ2SEQ: labels.TextLabel,
        IMAGE_CLASSIFICATION: labels.CategoryLabel,
        SPEECH2TEXT: labels.TextLabel,
    }
    if project_type not in mapping:
        ValueError(f"Invalid project type: {project_type}")
    return mapping[project_type]


def create_cleaner(project):
    mapping = {
        DOCUMENT_CLASSIFICATION: cleaners.CategoryCleaner,
        SEQUENCE_LABELING: cleaners.SpanCleaner,
        IMAGE_CLASSIFICATION: cleaners.CategoryCleaner,
    }
    if project.project_type not in mapping:
        return cleaners.Cleaner(project)
    cleaner_class = mapping.get(project.project_type, cleaners.Cleaner)
    return cleaner_class(project)


def select_examples(project):
    use_relation = getattr(project, "use_relation", False)
    if project.project_type == SEQUENCE_LABELING and use_relation:
        return labeled_examples.RelationExamples
    if project.project_type == SEQUENCE_LABELING:
        return labeled_examples.SpanExamples
    elif project.project_type == DOCUMENT_CLASSIFICATION:
        return labeled_examples.CategoryExamples
    elif project.project_type == SEQ2SEQ:
        return labeled_examples.TextExamples
    elif project.project_type == INTENT_DETECTION_AND_SLOT_FILLING:
        return labeled_examples.SpanAndCategoryExamples
    else:
        return labeled_examples.LabeledExamples


def create_data_formatter(project: Project, column_data: str = readers.DEFAULT_TEXT_COLUMN, **kwargs) -> DataFormatter:
    data_class = get_data_class(project.project_type)
    return DataFormatter(column=column_data, data_class=data_class)


def create_label_formatters(
    project: Project, column_label: str = readers.DEFAULT_LABEL_COLUMN, **kwargs
) -> List[LabelFormatter]:
    use_relation = getattr(project, "use_relation", False)
    if project.project_type == INTENT_DETECTION_AND_SLOT_FILLING:
        return [
            LabelFormatter(column="entities", label_class=labels.SpanLabel),
            LabelFormatter(column="cats", label_class=labels.CategoryLabel),
        ]
    elif project.project_type == SEQUENCE_LABELING and use_relation:
        return [
            LabelFormatter(column="entities", label_class=labels.SpanLabel),
            LabelFormatter(column="relations", label_class=labels.RelationLabel),
        ]
    else:
        label_class = get_label_class(project.project_type)
        return [LabelFormatter(column=column_label, label_class=label_class)]


def create_builder(project, **kwargs):
    if not project.is_text_project:
        return builders.PlainBuilder(data_class=get_data_class(project.project_type))

    data_column = builders.DataColumn(
        name=kwargs.get("column_data") or readers.DEFAULT_TEXT_COLUMN, value_class=get_data_class(project.project_type)
    )
    use_relation = getattr(project, "use_relation", False)
    # If project is intent detection and slot filling,
    # column names are fixed: entities, cats
    if project.project_type == INTENT_DETECTION_AND_SLOT_FILLING:
        label_columns = [
            builders.LabelColumn(name="cats", value_class=labels.CategoryLabel),
            builders.LabelColumn(name="entities", value_class=labels.SpanLabel),
        ]
    elif project.project_type == SEQUENCE_LABELING and use_relation:
        label_columns = [
            builders.LabelColumn(name="entities", value_class=labels.SpanLabel),
            builders.LabelColumn(name="relations", value_class=labels.RelationLabel),
        ]
    else:
        label_columns = [
            builders.LabelColumn(
                name=kwargs.get("column_label") or readers.DEFAULT_LABEL_COLUMN,
                value_class=get_label_class(project.project_type),
            )
        ]
    builder = builders.ColumnBuilder(data_column=data_column, label_columns=label_columns)
    return builder
