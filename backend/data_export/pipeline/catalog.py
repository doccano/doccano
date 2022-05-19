from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Type

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


class FastText(Format):
    name = "fastText"


class JSON(Format):
    name = "JSON"


class JSONL(Format):
    name = "JSONL"


class Options:
    options: Dict[str, List] = defaultdict(list)

    @classmethod
    def filter_by_task(cls, task_name: str, use_relation: bool = False):
        options = cls.options[task_name]
        return [
            {**file_format.dict(), "example": example}
            for file_format, example, use_rel in options
            if use_rel == use_relation
        ]

    @classmethod
    def register(cls, task: str, file_format: Type[Format], file: Path, use_relation: bool = False):
        example = cls.load_example(file)
        cls.options[task].append((file_format, example, use_relation))

    @staticmethod
    def load_example(file):
        with open(file, encoding="utf-8") as f:
            return f.read()


# Text Classification
TEXT_CLASSIFICATION_DIR = EXAMPLE_DIR / "text_classification"
Options.register(DOCUMENT_CLASSIFICATION, CSV, TEXT_CLASSIFICATION_DIR / "example.csv")
Options.register(DOCUMENT_CLASSIFICATION, FastText, TEXT_CLASSIFICATION_DIR / "example.txt")
Options.register(DOCUMENT_CLASSIFICATION, JSON, TEXT_CLASSIFICATION_DIR / "example.json")
Options.register(DOCUMENT_CLASSIFICATION, JSONL, TEXT_CLASSIFICATION_DIR / "example.jsonl")

# Sequence Labeling
SEQUENCE_LABELING_DIR = EXAMPLE_DIR / "sequence_labeling"
RELATION_EXTRACTION_DIR = EXAMPLE_DIR / "relation_extraction"
Options.register(SEQUENCE_LABELING, JSONL, SEQUENCE_LABELING_DIR / "example.jsonl")
Options.register(SEQUENCE_LABELING, JSONL, RELATION_EXTRACTION_DIR / "example.jsonl", True)

# Sequence to sequence
SEQ2SEQ_DIR = EXAMPLE_DIR / "sequence_to_sequence"
Options.register(SEQ2SEQ, CSV, SEQ2SEQ_DIR / "example.csv")
Options.register(SEQ2SEQ, JSON, SEQ2SEQ_DIR / "example.json")
Options.register(SEQ2SEQ, JSONL, SEQ2SEQ_DIR / "example.jsonl")

# Intent detection and slot filling
INTENT_DETECTION_DIR = EXAMPLE_DIR / "intent_detection"
Options.register(INTENT_DETECTION_AND_SLOT_FILLING, JSONL, INTENT_DETECTION_DIR / "example.jsonl")

# Image Classification
IMAGE_CLASSIFICATION_DIR = EXAMPLE_DIR / "image_classification"
Options.register(IMAGE_CLASSIFICATION, JSONL, IMAGE_CLASSIFICATION_DIR / "example.jsonl")

# Speech to Text
SPEECH2TEXT_DIR = EXAMPLE_DIR / "speech_to_text"
Options.register(SPEECH2TEXT, JSONL, SPEECH2TEXT_DIR / "example.jsonl")
