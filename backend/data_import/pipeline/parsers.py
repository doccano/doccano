import csv
import io
import json
import os
from typing import Any, Dict, Iterator, List, Tuple

import chardet
import pyexcel
import pyexcel.exceptions
from chardet import UniversalDetector
from seqeval.scheme import BILOU, IOB2, IOBES, IOE2, Tokens

from .exceptions import FileParseException
from .readers import (
    DEFAULT_LABEL_COLUMN,
    DEFAULT_TEXT_COLUMN,
    LINE_NUMBER_COLUMN,
    Parser,
)

DEFAULT_ENCODING = "Auto"


def detect_encoding(filename: str, buffer_size: int = io.DEFAULT_BUFFER_SIZE) -> str:
    """Detects character encoding automatically.

    If you want to know the supported encodings, please see the following document:
    https://chardet.readthedocs.io/en/latest/supported-encodings.html

    Args:
        filename: the filename for detecting the encoding.
        buffer_size: the buffer size to read file contents incrementally.

    Returns:
        The character encoding.
    """
    # For a small file.
    if os.path.getsize(filename) < buffer_size:
        detected = chardet.detect(open(filename, "rb").read())
        return detected.get("encoding", "utf-8")

    # For a large file, call the Universal Encoding Detector incrementally.
    # It will stop as soon as it is confident enough to report its results.
    # See: https://chardet.readthedocs.io/en/latest/usage.html
    with open(filename, "rb") as f:
        detector = UniversalDetector()
        while True:
            binary = f.read(buffer_size)
            detector.feed(binary)
            if binary == b"":
                break
            if detector.done:
                break
        if detector.done:
            return detector.result["encoding"] or "utf-8"
        else:
            return "utf-8"


def decide_encoding(filename: str, encoding: str) -> str:
    """Decide character encoding automatically.

    If the encoding is DEFAULT_ENCODING, detects it automatically.
    Otherwise, return it as is.

    Args:
         filename: The filename for decide the encoding.
         encoding: The specified encoding.

    Returns:
        The character encoding.
    """
    if encoding == DEFAULT_ENCODING:
        return detect_encoding(filename)
    else:
        return encoding


class LineReader:
    """LineReader is a helper class to read a file line by line.

    Attributes:
        filename: The filename to read.
        encoding: The character encoding.
    """

    def __init__(self, filename: str, encoding: str = DEFAULT_ENCODING):
        self.filename = filename
        self.encoding = encoding

    def __iter__(self) -> Iterator[str]:
        encoding = decide_encoding(self.filename, self.encoding)
        with open(self.filename, encoding=encoding) as f:
            for line in f:
                yield line.rstrip()


class PlainParser(Parser):
    """PlainParser is a parser simply returns a dictionary.

    This is for a task without any text.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        yield {}


class LineParser(Parser):
    """LineParser is a parser to read a file line by line.

    Attributes:
        encoding: The character encoding.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING, **kwargs):
        self.encoding = encoding

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        reader = LineReader(filename, self.encoding)
        for line_num, line in enumerate(reader, start=1):
            yield {DEFAULT_TEXT_COLUMN: line, LINE_NUMBER_COLUMN: line_num}


class TextFileParser(Parser):
    """TextFileParser is a parser to read an entire file content.

    Attributes:
        encoding: The character encoding.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING, **kwargs):
        self.encoding = encoding

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        encoding = decide_encoding(filename, self.encoding)
        with open(filename, encoding=encoding) as f:
            yield {DEFAULT_TEXT_COLUMN: f.read()}


class CSVParser(Parser):
    """CSVParser is a parser to read a csv file and return its rows.

    Attributes:
        encoding: The character encoding.
        delimiter: A one-character string used to separate fields. It defaults to ','.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING, delimiter: str = ",", **kwargs):
        self.encoding = encoding
        self.delimiter = delimiter

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        encoding = decide_encoding(filename, self.encoding)
        with open(filename, encoding=encoding) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            for line_num, row in enumerate(reader, start=1):
                yield {LINE_NUMBER_COLUMN: line_num, **row}


class JSONParser(Parser):
    """JSONParser is a parser to read a json file and return its rows.

    Attributes:
        encoding: The character encoding.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING, **kwargs):
        self.encoding = encoding
        self._errors: List[FileParseException] = []

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        encoding = decide_encoding(filename, self.encoding)
        with open(filename, encoding=encoding) as f:
            try:
                rows = json.load(f)
                for row in rows:
                    yield row
            except json.decoder.JSONDecodeError as e:
                error = FileParseException(filename, line_num=1, message=str(e))
                self._errors.append(error)

    @property
    def errors(self) -> List[FileParseException]:
        return self._errors


class JSONLParser(Parser):
    """JSONLParser is a parser to read a JSONL file and return its rows.

    Attributes:
        encoding: The character encoding.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING, **kwargs):
        self.encoding = encoding
        self._errors: List[FileParseException] = []

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        reader = LineReader(filename, self.encoding)
        for line_num, line in enumerate(reader, start=1):
            try:
                row = json.loads(line)
                yield {LINE_NUMBER_COLUMN: line_num, **row}
            except json.decoder.JSONDecodeError as e:
                error = FileParseException(filename, line_num, str(e))
                self._errors.append(error)

    @property
    def errors(self) -> List[FileParseException]:
        return self._errors


class ExcelParser(Parser):
    """ExcelParser is a parser to read a excel file."""

    def __init__(self, **kwargs):
        self._errors = []

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        rows = pyexcel.iget_records(file_name=filename)
        try:
            for line_num, row in enumerate(rows, start=1):
                yield {LINE_NUMBER_COLUMN: line_num, **row}
        except pyexcel.exceptions.FileTypeNotSupported as e:
            error = FileParseException(filename, line_num=1, message=str(e))
            self._errors.append(error)

    @property
    def errors(self) -> List[FileParseException]:
        return self._errors


class FastTextParser(Parser):
    """FastTextParser is a parser to read a fastText format and returns a text and labels.

    The example format is as follows:
        __label__positive I really enjoyed this restaurant.
    This format expects the category first, with the prefix ‘__label__’ before each category,
    and then the input text, like so,

    Attributes:
        encoding: The character encoding.
        label: The label prefix. It defaults to `__label__`.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING, label: str = "__label__", **kwargs):
        self.encoding = encoding
        self.label = label

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        reader = LineReader(filename, self.encoding)
        for line_num, line in enumerate(reader, start=1):
            labels = []
            tokens = []
            for token in line.rstrip().split(" "):
                if token.startswith(self.label):
                    label_name = token[len(self.label) :]
                    labels.append(label_name)
                else:
                    tokens.append(token)
            text = " ".join(tokens)
            yield {DEFAULT_TEXT_COLUMN: text, DEFAULT_LABEL_COLUMN: labels, LINE_NUMBER_COLUMN: line_num}


class CoNLLParser(Parser):
    """CoNLLParser is a parser to read conll like format and returns a text and labels.

    The example format is as follows:
        EU  B-ORG
        rejects O
        German  B-MISC
        call  O
        to  O
        boycott O
        British B-MISC
        lamb  O
        . O

        Peter B-PER
        Blackburn I-PER
    This format expects a token in the first column, and a tag in the second column.
    The each data is separated by a new line.

    Attributes:
        encoding: The character encoding.
        delimiter: A one-character string used to separate fields. It defaults to ' '.
        scheme: The tagging scheme. It supports `IOB2`, `IOE2`, `IOBES`, and `BILOU`.
    """

    def __init__(self, encoding: str = DEFAULT_ENCODING, delimiter: str = " ", scheme: str = "IOB2", **kwargs):
        self.encoding = encoding
        self.delimiter = delimiter
        mapping = {"IOB2": IOB2, "IOE2": IOE2, "IOBES": IOBES, "BILOU": BILOU}
        self._errors: List[FileParseException] = []
        if scheme in mapping:
            self.scheme = mapping[scheme]
        else:
            self.scheme = None

    @property
    def errors(self) -> List[FileParseException]:
        return self._errors

    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        if not self.scheme:
            message = "The specified scheme is not supported."
            error = FileParseException(filename, line_num=1, message=message)
            self._errors.append(error)
            return

        reader = LineReader(filename, self.encoding)
        words, tags = [], []
        for line_num, line in enumerate(reader, start=1):
            line = line.rstrip()
            if line:
                tokens = line.split("\t")
                if len(tokens) != 2:
                    message = "A line must be separated by tab and has two columns."
                    self._errors.append(FileParseException(filename, line_num, message))
                    return
                word, tag = tokens
                words.append(word)
                tags.append(tag)
            else:
                yield self.create_record(tags, words)
                words, tags = [], []
        if words:
            yield self.create_record(tags, words)

    def create_record(self, tags, words):
        text = self.delimiter.join(words)
        labels = self.align_span(words, tags)
        return {DEFAULT_TEXT_COLUMN: text, DEFAULT_LABEL_COLUMN: labels}

    def align_span(self, words: List[str], tags: List[str]) -> List[Tuple[int, int, str]]:
        tokens = Tokens(tags, self.scheme)
        labels = []
        for entity in tokens.entities:
            text = self.delimiter.join(words[: entity.start])
            start = len(text) + len(self.delimiter) if text else len(text)
            chunk = words[entity.start : entity.end]
            text = self.delimiter.join(chunk)
            end = start + len(text)
            labels.append((start, end, entity.tag))
        return labels
