from collections import defaultdict
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from ...models import (DOCUMENT_CLASSIFICATION, IMAGE_CLASSIFICATION, SEQ2SEQ,
                       SEQUENCE_LABELING)
from . import examples


class Format:
    name = ''

    @classmethod
    def dict(cls):
        return {
            'name': cls.name,
        }


class CSV(Format):
    name = 'CSV'
    extension = 'csv'


class FastText(Format):
    name = 'fastText'
    extension = 'txt'


class JSON(Format):
    name = 'JSON'
    extension = 'json'


class JSONL(Format):
    name = 'JSONL'
    extension = 'jsonl'


class OptionDelimiter(BaseModel):
    delimiter: Literal[',', '\t', ';', '|', ' '] = ','


class OptionNone(BaseModel):
    pass


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
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter, examples.Category_CSV)
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionNone, examples.Category_fastText)
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionNone, examples.Category_JSON)
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionNone, examples.Category_JSONL)

# Sequence Labeling
Options.register(SEQUENCE_LABELING, JSONL, OptionNone, examples.Offset_JSONL)

# Sequence to sequence
Options.register(SEQ2SEQ, CSV, OptionDelimiter, examples.Text_CSV)
Options.register(SEQ2SEQ, JSON, OptionNone, examples.Text_JSON)
Options.register(SEQ2SEQ, JSONL, OptionNone, examples.Text_JSONL)

# Image Classification
Options.register(IMAGE_CLASSIFICATION, JSONL, OptionNone, examples.CategoryImageClassification)
