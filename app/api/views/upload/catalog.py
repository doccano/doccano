from collections import defaultdict
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from . import examples
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


class TextFile(Format):
    name = 'TextFile'
    accept_types = 'text/*'


class TextLine(Format):
    name = 'TextLine'
    accept_types = 'text/*'


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
    delimiter: Literal[' ', ''] = ' '


class Options:
    options: Dict[str, List] = defaultdict(list)

    @classmethod
    def filter_by_task(cls, task_name: str):
        options = cls.options[task_name]
        return [
            {
                **format.dict(),
                **option.schema(),
                'example': example
            } for format, option, example in options
        ]

    @classmethod
    def register(cls,
                 task: str,
                 format: Type[Format],
                 option: Type[BaseModel],
                 example: str):
        cls.options[task].append((format, option, example))


# Text Classification
Options.register(DOCUMENT_CLASSIFICATION, TextFile, OptionNone, examples.Generic_TextFile)
Options.register(DOCUMENT_CLASSIFICATION, TextLine, OptionNone, examples.Generic_TextLine)
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter, examples.Category_CSV)
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionNone, examples.Category_fastText)
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionColumn, examples.Category_JSON)
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionColumn, examples.Category_JSONL)
Options.register(DOCUMENT_CLASSIFICATION, Excel, OptionColumn, examples.Category_CSV)

# Sequence Labeling
Options.register(SEQUENCE_LABELING, TextFile, OptionNone, examples.Generic_TextFile)
Options.register(SEQUENCE_LABELING, TextLine, OptionNone, examples.Generic_TextLine)
Options.register(SEQUENCE_LABELING, JSONL, OptionColumn, examples.Offset_JSONL)
Options.register(SEQUENCE_LABELING, CoNLL, OptionCoNLL, examples.Offset_CoNLL)

# Sequence to sequence
Options.register(SEQ2SEQ, TextFile, OptionNone, examples.Generic_TextFile)
Options.register(SEQ2SEQ, TextLine, OptionNone, examples.Generic_TextLine)
Options.register(SEQ2SEQ, CSV, OptionDelimiter, examples.Text_CSV)
Options.register(SEQ2SEQ, JSON, OptionColumn, examples.Text_JSON)
Options.register(SEQ2SEQ, JSONL, OptionColumn, examples.Text_JSONL)
Options.register(SEQ2SEQ, Excel, OptionColumn, examples.Text_CSV)
