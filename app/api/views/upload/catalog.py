from collections import defaultdict
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from ...models import DOCUMENT_CLASSIFICATION, SEQ2SEQ, SEQUENCE_LABELING

CSV = 'CSV'
FastText = 'fastText'
JSON = 'JSON'
JSONL = 'JSONL'
EXCEL = 'Excel'
CoNLL = 'CoNLL'


class OptionColumn(BaseModel):
    column_data: str = 'text'
    column_label: str = 'label'


class OptionDelimiter(OptionColumn):
    delimiter: Literal[',', '\t', ';', '|', ' '] = ','


class OptionNone(BaseModel):
    pass


class Options:
    options: Dict[str, List] = defaultdict(list)

    @classmethod
    def filter_by_task(cls, task_name: str):
        options = cls.options[task_name]
        return [{'name': name, **option.schema()} for name, option in options]

    @classmethod
    def register(cls, task: str, name: str, option: Type[BaseModel]):
        cls.options[task].append((name, option))


# Text Classification
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter)
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionNone)
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionColumn)
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionColumn)
Options.register(DOCUMENT_CLASSIFICATION, EXCEL, OptionColumn)

# Sequence Labeling
Options.register(SEQUENCE_LABELING, JSONL, OptionColumn)
Options.register(SEQUENCE_LABELING, CoNLL, OptionNone)

# Sequence to sequence
Options.register(SEQ2SEQ, CSV, OptionDelimiter)
Options.register(SEQ2SEQ, JSON, OptionColumn)
Options.register(SEQ2SEQ, JSONL, OptionColumn)
Options.register(SEQ2SEQ, EXCEL, OptionColumn)
