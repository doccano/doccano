from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from projects.models import (
    DOCUMENT_CLASSIFICATION,
    IMAGE_CLASSIFICATION,
    INTENT_DETECTION_AND_SLOT_FILLING,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
)

EXAMPLE_DIR = Path(__file__).parent.resolve() / "examples"


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
    def register(cls, task: str, file_format: Type[Format], option: Type[BaseModel], file: Path):
        example = cls.load_example(file)
        cls.options[task].append((file_format, option, example))

    @staticmethod
    def load_example(file):
        with open(file, encoding="utf-8") as f:
            return f.read()


# Text Classification
TEXT_CLASSIFICATION_DIR = EXAMPLE_DIR / "text_classification"
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter, TEXT_CLASSIFICATION_DIR / "example.csv")
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionNone, TEXT_CLASSIFICATION_DIR / "example.txt")
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionNone, TEXT_CLASSIFICATION_DIR / "example.json")
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionNone, TEXT_CLASSIFICATION_DIR / "example.jsonl")

# Sequence Labeling
SEQUENCE_LABELING_DIR = EXAMPLE_DIR / "sequence_labeling"
RELATION_EXTRACTION_DIR = EXAMPLE_DIR / "relation_extraction"
Options.register(SEQUENCE_LABELING, JSONL, OptionNone, SEQUENCE_LABELING_DIR / "example.jsonl")
Options.register(SEQUENCE_LABELING, JSONL, OptionNone, RELATION_EXTRACTION_DIR / "example.jsonl")

# Sequence to sequence
SEQ2SEQ_DIR = EXAMPLE_DIR / "sequence_to_sequence"
Options.register(SEQ2SEQ, CSV, OptionDelimiter, SEQ2SEQ_DIR / "example.csv")
Options.register(SEQ2SEQ, JSON, OptionNone, SEQ2SEQ_DIR / "example.json")
Options.register(SEQ2SEQ, JSONL, OptionNone, SEQ2SEQ_DIR / "example.jsonl")

# Intent detection and slot filling
INTENT_DETECTION_DIR = EXAMPLE_DIR / "intent_detection"
Options.register(INTENT_DETECTION_AND_SLOT_FILLING, JSONL, OptionNone, INTENT_DETECTION_DIR / "example.jsonl")

# Image Classification
IMAGE_CLASSIFICATION_DIR = EXAMPLE_DIR / "image_classification"
Options.register(IMAGE_CLASSIFICATION, JSONL, OptionNone, IMAGE_CLASSIFICATION_DIR / "example.jsonl")

# Speech to Text
SPEECH2TEXT_DIR = EXAMPLE_DIR / "speech_to_text"
Options.register(SPEECH2TEXT, JSONL, OptionNone, SPEECH2TEXT_DIR / "example.jsonl")
