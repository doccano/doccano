from collections import defaultdict
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from . import examples
from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
)


class Format:
    name = ""

    @classmethod
    def dict(cls):
        return {
            "name": cls.name,
        }


class CSV(Format):
    name = "CSV"
    extension = "csv"


class FastText(Format):
    name = "fastText"
    extension = "txt"


class JSON(Format):
    name = "JSON"
    extension = "json"


class JSONL(Format):
    name = "JSONL"
    extension = "jsonl"


class IntentAndSlot(Format):
    name = "JSONL(intent and slot)"
    extension = "jsonl"


class JSONLRelation(Format):
    name = "JSONL(relation)"
    extension = "jsonl"


class OptionDelimiter(BaseModel):
    delimiter: Literal[",", "\t", ";", "|", " "] = ","


class OptionNone(BaseModel):
    pass


class Options:
    options: Dict[str, List] = defaultdict(list)

    @classmethod
    def filter_by_task(cls, task_name: str):
        options = cls.options[task_name]
        return [
            {**file_format.dict(), **option.schema(), "example": example} for file_format, option, example in options
        ]

    @classmethod
    def register(cls, task: str, file_format: Type[Format], option: Type[BaseModel], example: str):
        cls.options[task].append((file_format, option, example))


# Text Classification
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter, examples.CATEGORY_CSV)
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionNone, examples.CATEGORY_FASTTEXT)
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionNone, examples.CATEGORY_JSON)
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionNone, examples.CATEGORY_JSONL)

# Sequence Labeling
Options.register(SEQUENCE_LABELING, JSONL, OptionNone, examples.SPAN_JSONL)
Options.register(SEQUENCE_LABELING, JSONL, OptionNone, examples.ENTITY_AND_RELATION_JSONL)

# Sequence to sequence
Options.register(SEQ2SEQ, CSV, OptionDelimiter, examples.TEXT_CSV)
Options.register(SEQ2SEQ, JSON, OptionNone, examples.TEXT_JSON)
Options.register(SEQ2SEQ, JSONL, OptionNone, examples.TEXT_JSONL)

# Intent detection and slot filling
Options.register(INTENT_DETECTION_AND_SLOT_FILLING, JSONL, OptionNone, examples.INTENT_JSONL)

# Image Classification
Options.register(IMAGE_CLASSIFICATION, JSONL, OptionNone, examples.CATEGORY_IMAGE_CLASSIFICATION)

# Speech to Text
Options.register(SPEECH2TEXT, JSONL, OptionNone, examples.SPEECH_TO_TEXT)
