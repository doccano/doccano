from collections import defaultdict
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from ...models import DOCUMENT_CLASSIFICATION, SEQ2SEQ, SEQUENCE_LABELING


class Format:
    name = ''
    accept_types = ''

    @classmethod
    def dict(cls):
        return {
            'name': cls.name,
            'accept_types': cls.accept_types
        }


class CSV(Format):
    name = 'CSV'
    accept_types = 'text/csv'


class FastText(Format):
    name = 'fastText'
    accept_types = 'text/plain'


class JSON(Format):
    name = 'JSON'
    accept_types = 'application/json'


class JSONL(Format):
    name = 'JSONL'
    accept_types = 'application/jsonl'


class Excel(Format):
    name = 'Excel'
    accept_types = 'application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class CoNLL(Format):
    name = 'CoNLL'
    accept_types = 'text/*'


class OptionColumn(BaseModel):
    column_data: str = 'text'
    column_label: str = 'label'


class OptionDelimiter(OptionColumn):
    delimiter: Literal[',', '\t', ';', '|', ' '] = ','


class OptionNone(BaseModel):
    pass


class OptionCoNLL(BaseModel):
    scheme: Literal['IOB2', 'IOE2', 'IOBES', 'BILOU'] = 'IOB2'


class Options:
    options: Dict[str, List] = defaultdict(list)

    @classmethod
    def filter_by_task(cls, task_name: str):
        options = cls.options[task_name]
        return [{**format.dict(), **option.schema()} for format, option in options]

    @classmethod
    def register(cls, task: str, format: Type[Format], option: Type[BaseModel]):
        cls.options[task].append((format, option))


# Text Classification
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter)
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionNone)
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionColumn)
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionColumn)
Options.register(DOCUMENT_CLASSIFICATION, Excel, OptionColumn)

# Sequence Labeling
Options.register(SEQUENCE_LABELING, JSONL, OptionColumn)
Options.register(SEQUENCE_LABELING, CoNLL, OptionNone)

# Sequence to sequence
Options.register(SEQ2SEQ, CSV, OptionDelimiter)
Options.register(SEQ2SEQ, JSON, OptionColumn)
Options.register(SEQ2SEQ, JSONL, OptionColumn)
Options.register(SEQ2SEQ, Excel, OptionColumn)
