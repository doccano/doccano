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
encodings = Literal[
    "Auto",
    "ascii",
    "big5",
    "big5hkscs",
    "cp037",
    "cp273",
    "cp424",
    "cp437",
    "cp500",
    "cp720",
    "cp737",
    "cp775",
    "cp850",
    "cp852",
    "cp855",
    "cp856",
    "cp857",
    "cp858",
    "cp860",
    "cp861",
    "cp862",
    "cp863",
    "cp864",
    "cp865",
    "cp866",
    "cp869",
    "cp874",
    "cp875",
    "cp932",
    "cp949",
    "cp950",
    "cp1006",
    "cp1026",
    "cp1125",
    "cp1140",
    "cp1250",
    "cp1251",
    "cp1252",
    "cp1253",
    "cp1254",
    "cp1255",
    "cp1256",
    "cp1257",
    "cp1258",
    "cp65001",
    "euc_jp",
    "euc_jis_2004",
    "euc_jisx0213",
    "euc_kr",
    "gb2312",
    "gbk",
    "gb18030",
    "hz",
    "iso2022_jp",
    "iso2022_jp_1",
    "iso2022_jp_2",
    "iso2022_jp_2004",
    "iso2022_jp_3",
    "iso2022_jp_ext",
    "iso2022_kr",
    "latin_1",
    "iso8859_2",
    "iso8859_3",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "iso8859_10",
    "iso8859_11",
    "iso8859_13",
    "iso8859_14",
    "iso8859_15",
    "iso8859_16",
    "johab",
    "koi8_r",
    "koi8_t",
    "koi8_u",
    "kz1048",
    "mac_cyrillic",
    "mac_greek",
    "mac_iceland",
    "mac_latin2",
    "mac_roman",
    "mac_turkish",
    "ptcp154",
    "shift_jis",
    "shift_jis_2004",
    "shift_jisx0213",
    "utf_32",
    "utf_32_be",
    "utf_32_le",
    "utf_16",
    "utf_16_be",
    "utf_16_le",
    "utf_7",
    "utf_8",
    "utf_8_sig",
]


class Format:
    name = ""
    accept_types = ""

    @classmethod
    def dict(cls):
        return {"name": cls.name, "accept_types": cls.accept_types}


class CSV(Format):
    name = "CSV"
    accept_types = "text/csv"


class FastText(Format):
    name = "fastText"
    accept_types = "text/plain"


class JSON(Format):
    name = "JSON"
    accept_types = "application/json"


class JSONL(Format):
    name = "JSONL"
    accept_types = "*"


class Excel(Format):
    name = "Excel"
    accept_types = "application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


class TextFile(Format):
    name = "TextFile"
    accept_types = "text/*"


class TextLine(Format):
    name = "TextLine"
    accept_types = "text/*"


class CoNLL(Format):
    name = "CoNLL"
    accept_types = "text/*"


class ImageFile(Format):
    name = "ImageFile"
    accept_types = "image/png, image/jpeg, image/bmp, image/gif"


class AudioFile(Format):
    name = "AudioFile"
    accept_types = "audio/ogg, audio/aac, audio/mpeg, audio/wav"


class OptionColumn(BaseModel):
    encoding: encodings = "utf_8"
    column_data: str = "text"
    column_label: str = "label"


class OptionDelimiter(OptionColumn):
    encoding: encodings = "utf_8"
    delimiter: Literal[",", "\t", ";", "|", " "] = ","


class OptionEncoding(BaseModel):
    encoding: encodings = "utf_8"


class OptionCoNLL(BaseModel):
    encoding: encodings = "utf_8"
    scheme: Literal["IOB2", "IOE2", "IOBES", "BILOU"] = "IOB2"
    delimiter: Literal[" ", ""] = " "


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
    def load_example(file) -> str:
        with open(file, encoding="utf-8") as f:
            return f.read()


TASK_AGNOSTIC_DIR = EXAMPLE_DIR / "task_agnostic"
TEXT_CLASSIFICATION_DIR = EXAMPLE_DIR / "text_classification"
Options.register(DOCUMENT_CLASSIFICATION, TextFile, OptionEncoding, TASK_AGNOSTIC_DIR / "text_files.txt")
Options.register(DOCUMENT_CLASSIFICATION, TextLine, OptionEncoding, TASK_AGNOSTIC_DIR / "text_lines.txt")
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter, TEXT_CLASSIFICATION_DIR / "example.csv")
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionEncoding, TEXT_CLASSIFICATION_DIR / "example.txt")
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionColumn, TEXT_CLASSIFICATION_DIR / "example.json")
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionColumn, TEXT_CLASSIFICATION_DIR / "example.jsonl")
Options.register(DOCUMENT_CLASSIFICATION, Excel, OptionColumn, TEXT_CLASSIFICATION_DIR / "example.csv")

SEQUENCE_LABELING_DIR = EXAMPLE_DIR / "sequence_labeling"
Options.register(SEQUENCE_LABELING, TextFile, OptionEncoding, TASK_AGNOSTIC_DIR / "text_files.txt")
Options.register(SEQUENCE_LABELING, TextLine, OptionEncoding, TASK_AGNOSTIC_DIR / "text_lines.txt")
Options.register(SEQUENCE_LABELING, JSONL, OptionColumn, SEQUENCE_LABELING_DIR / "example.jsonl")
Options.register(SEQUENCE_LABELING, CoNLL, OptionCoNLL, SEQUENCE_LABELING_DIR / "example.txt")

SEQ2SEQ_DIR = EXAMPLE_DIR / "sequence_to_sequence"
Options.register(SEQ2SEQ, TextFile, OptionEncoding, TASK_AGNOSTIC_DIR / "text_files.txt")
Options.register(SEQ2SEQ, TextLine, OptionEncoding, TASK_AGNOSTIC_DIR / "text_lines.txt")
Options.register(SEQ2SEQ, CSV, OptionDelimiter, SEQ2SEQ_DIR / "example.csv")
Options.register(SEQ2SEQ, JSON, OptionColumn, SEQ2SEQ_DIR / "example.json")
Options.register(SEQ2SEQ, JSONL, OptionColumn, SEQ2SEQ_DIR / "example.jsonl")
Options.register(SEQ2SEQ, Excel, OptionColumn, SEQ2SEQ_DIR / "example.csv")

INTENT_DETECTION_DIR = EXAMPLE_DIR / "intent_detection"
Options.register(INTENT_DETECTION_AND_SLOT_FILLING, TextFile, OptionEncoding, TASK_AGNOSTIC_DIR / "text_files.txt")
Options.register(INTENT_DETECTION_AND_SLOT_FILLING, TextLine, OptionEncoding, TASK_AGNOSTIC_DIR / "text_lines.txt")
Options.register(INTENT_DETECTION_AND_SLOT_FILLING, JSONL, OptionNone, INTENT_DETECTION_DIR / "example.jsonl")

IMAGE_CLASSIFICATION_DIR = EXAMPLE_DIR / "image_classification"
Options.register(IMAGE_CLASSIFICATION, ImageFile, OptionNone, IMAGE_CLASSIFICATION_DIR / "image_files.txt")

SPEECH_TO_TEXT_DIR = EXAMPLE_DIR / "speech_to_text"
Options.register(SPEECH2TEXT, AudioFile, OptionNone, SPEECH_TO_TEXT_DIR / "audio_files.txt")
