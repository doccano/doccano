from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from .exceptions import FileFormatException
from projects.models import ProjectType

# Define the example directories
EXAMPLE_DIR = Path(__file__).parent.resolve() / "examples"
TASK_AGNOSTIC_DIR = EXAMPLE_DIR / "task_agnostic"
TEXT_CLASSIFICATION_DIR = EXAMPLE_DIR / "text_classification"
SEQUENCE_LABELING_DIR = EXAMPLE_DIR / "sequence_labeling"
RELATION_EXTRACTION_DIR = EXAMPLE_DIR / "relation_extraction"
SEQ2SEQ_DIR = EXAMPLE_DIR / "sequence_to_sequence"
INTENT_DETECTION_DIR = EXAMPLE_DIR / "intent_detection"
IMAGE_CLASSIFICATION_DIR = EXAMPLE_DIR / "image_classification"
SPEECH_TO_TEXT_DIR = EXAMPLE_DIR / "speech_to_text"

# Define the task identifiers
RELATION_EXTRACTION = "RelationExtraction"

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

    def validate_mime(self, mime: str):
        return True

    @staticmethod
    def is_plain_text():
        return False


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

    @staticmethod
    def is_plain_text():
        return True


class TextLine(Format):
    name = "TextLine"
    accept_types = "text/*"

    @staticmethod
    def is_plain_text():
        return True


class CoNLL(Format):
    name = "CoNLL"
    accept_types = "text/*"


class ImageFile(Format):
    name = "ImageFile"
    accept_types = "image/png, image/jpeg, image/bmp, image/gif"

    def validate_mime(self, mime: str):
        return mime in self.accept_types


class AudioFile(Format):
    name = "AudioFile"
    accept_types = "audio/ogg, audio/aac, audio/mpeg, audio/wav"

    def validate_mime(self, mime: str):
        return mime in self.accept_types


class ArgColumn(BaseModel):
    encoding: encodings = "utf_8"
    column_data: str = "text"
    column_label: str = "label"


class ArgDelimiter(ArgColumn):
    encoding: encodings = "utf_8"
    delimiter: Literal[",", "\t", ";", "|", " "] = ","


class ArgEncoding(BaseModel):
    encoding: encodings = "utf_8"


class ArgCoNLL(BaseModel):
    encoding: encodings = "utf_8"
    scheme: Literal["IOB2", "IOE2", "IOBES", "BILOU"] = "IOB2"
    delimiter: Literal[" ", ""] = " "


class ArgNone(BaseModel):
    pass


@dataclass
class Option:
    display_name: str
    task_id: str
    file_format: Type[Format]
    arg: Type[BaseModel]
    file: Path

    @property
    def example(self) -> str:
        with open(self.file, "r", encoding="utf-8") as f:
            return f.read()

    def dict(self) -> Dict:
        return {
            **self.file_format.dict(),
            **self.arg.schema(),
            "example": self.example,
            "task_id": self.task_id,
            "display_name": self.display_name,
        }


def create_file_format(file_format: str) -> Format:
    for format_class in Format.__subclasses__():
        if format_class.name == file_format:
            return format_class()
    raise FileFormatException(file_format)


class Options:
    options: Dict[str, List] = defaultdict(list)

    @classmethod
    def filter_by_task(cls, task_name: str, use_relation: bool = False):
        options = cls.options[task_name]
        if use_relation:
            options = cls.options[task_name] + cls.options[RELATION_EXTRACTION]
        return [option.dict() for option in options]

    @classmethod
    def register(cls, option: Option):
        cls.options[option.task_id].append(option)


# Text tasks
text_tasks = [
    ProjectType.DOCUMENT_CLASSIFICATION,
    ProjectType.SEQUENCE_LABELING,
    ProjectType.SEQ2SEQ,
    ProjectType.INTENT_DETECTION_AND_SLOT_FILLING,
]
for task_id in text_tasks:
    Options.register(
        Option(
            display_name=TextFile.name,
            task_id=task_id,
            file_format=TextFile,
            arg=ArgEncoding,
            file=TASK_AGNOSTIC_DIR / "text_files.txt",
        )
    )
    Options.register(
        Option(
            display_name=TextLine.name,
            task_id=task_id,
            file_format=TextLine,
            arg=ArgEncoding,
            file=TASK_AGNOSTIC_DIR / "text_lines.txt",
        )
    )

# Text Classification
Options.register(
    Option(
        display_name=CSV.name,
        task_id=ProjectType.DOCUMENT_CLASSIFICATION,
        file_format=CSV,
        arg=ArgDelimiter,
        file=TEXT_CLASSIFICATION_DIR / "example.csv",
    )
)
Options.register(
    Option(
        display_name=FastText.name,
        task_id=ProjectType.DOCUMENT_CLASSIFICATION,
        file_format=FastText,
        arg=ArgEncoding,
        file=TEXT_CLASSIFICATION_DIR / "example.txt",
    )
)
Options.register(
    Option(
        display_name=JSON.name,
        task_id=ProjectType.DOCUMENT_CLASSIFICATION,
        file_format=JSON,
        arg=ArgColumn,
        file=TEXT_CLASSIFICATION_DIR / "example.json",
    )
)
Options.register(
    Option(
        display_name=JSONL.name,
        task_id=ProjectType.DOCUMENT_CLASSIFICATION,
        file_format=JSONL,
        arg=ArgColumn,
        file=TEXT_CLASSIFICATION_DIR / "example.jsonl",
    )
)
Options.register(
    Option(
        display_name=Excel.name,
        task_id=ProjectType.DOCUMENT_CLASSIFICATION,
        file_format=Excel,
        arg=ArgColumn,
        file=TEXT_CLASSIFICATION_DIR / "example.csv",
    )
)

# Sequence Labelling
Options.register(
    Option(
        display_name=JSONL.name,
        task_id=ProjectType.SEQUENCE_LABELING,
        file_format=JSONL,
        arg=ArgColumn,
        file=SEQUENCE_LABELING_DIR / "example.jsonl",
    )
)
Options.register(
    Option(
        display_name=CoNLL.name,
        task_id=ProjectType.SEQUENCE_LABELING,
        file_format=CoNLL,
        arg=ArgCoNLL,
        file=SEQUENCE_LABELING_DIR / "example.txt",
    )
)

# Relation Extraction
Options.register(
    Option(
        display_name="JSONL(Relation)",
        task_id=RELATION_EXTRACTION,
        file_format=JSONL,
        arg=ArgNone,
        file=RELATION_EXTRACTION_DIR / "example.jsonl",
    )
)

# Seq2seq
Options.register(
    Option(
        display_name=CSV.name,
        task_id=ProjectType.SEQ2SEQ,
        file_format=CSV,
        arg=ArgDelimiter,
        file=SEQ2SEQ_DIR / "example.csv",
    )
)
Options.register(
    Option(
        display_name=JSON.name,
        task_id=ProjectType.SEQ2SEQ,
        file_format=JSON,
        arg=ArgColumn,
        file=SEQ2SEQ_DIR / "example.json",
    )
)
Options.register(
    Option(
        display_name=JSONL.name,
        task_id=ProjectType.SEQ2SEQ,
        file_format=JSONL,
        arg=ArgColumn,
        file=SEQ2SEQ_DIR / "example.jsonl",
    )
)
Options.register(
    Option(
        display_name=Excel.name,
        task_id=ProjectType.SEQ2SEQ,
        file_format=Excel,
        arg=ArgColumn,
        file=SEQ2SEQ_DIR / "example.csv",
    )
)

# Intent detection
Options.register(
    Option(
        display_name=JSONL.name,
        task_id=ProjectType.INTENT_DETECTION_AND_SLOT_FILLING,
        file_format=JSONL,
        arg=ArgNone,
        file=INTENT_DETECTION_DIR / "example.jsonl",
    )
)

# Image tasks
image_tasks = [
    ProjectType.IMAGE_CLASSIFICATION,
    ProjectType.IMAGE_CAPTIONING,
    ProjectType.BOUNDING_BOX,
    ProjectType.SEGMENTATION,
]
for task_name in image_tasks:
    Options.register(
        Option(
            display_name=ImageFile.name,
            task_id=task_name,
            file_format=ImageFile,
            arg=ArgNone,
            file=IMAGE_CLASSIFICATION_DIR / "image_files.txt",
        )
    )

# Speech to Text
Options.register(
    Option(
        display_name=AudioFile.name,
        task_id=ProjectType.SPEECH2TEXT,
        file_format=AudioFile,
        arg=ArgNone,
        file=SPEECH_TO_TEXT_DIR / "audio_files.txt",
    )
)
