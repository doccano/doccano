import abc
import collections.abc
import dataclasses
from typing import Any, Dict, Iterator, List, Type

from .cleaners import Cleaner
from .exceptions import FileParseException
from .labeled_examples import LabeledExamples, Record

DEFAULT_TEXT_COLUMN = "text"
DEFAULT_LABEL_COLUMN = "label"


class BaseReader(collections.abc.Iterable):
    """Reader has a role to parse files and return a Record iterator."""

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Record]:
        """Creates an iterator for elements of this dataset.

        Returns:
            A `Record` for the elements of this dataset.
        """
        raise NotImplementedError("Please implement this method in the subclass.")

    @property
    @abc.abstractmethod
    def errors(self):
        raise NotImplementedError("Please implement this method in the subclass.")

    @abc.abstractmethod
    def batch(self, batch_size: int, labeled_examples: Type[LabeledExamples]) -> Iterator[LabeledExamples]:
        raise NotImplementedError("Please implement this method in the subclass.")


class Parser(abc.ABC):
    """The abstract file parser."""

    @abc.abstractmethod
    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        """Parses the file and returns the dictionary."""
        raise NotImplementedError("Please implement this method in the subclass.")

    @property
    def errors(self) -> List[FileParseException]:
        """Returns parsing errors."""
        return []


@dataclasses.dataclass
class FileName:
    full_path: str
    generated_name: str
    upload_name: str


class Builder(abc.ABC):
    """The abstract Record builder."""

    @abc.abstractmethod
    def build(self, row: Dict[Any, Any], filename: FileName, line_num: int) -> Record:
        """Builds the record from the dictionary."""
        raise NotImplementedError("Please implement this method in the subclass.")


class Reader(BaseReader):
    def __init__(self, filenames: List[FileName], parser: Parser, builder: Builder, cleaner: Cleaner):
        self.filenames = filenames
        self.parser = parser
        self.builder = builder
        self.cleaner = cleaner
        self._errors: List[FileParseException] = []

    def __iter__(self) -> Iterator[Record]:
        for filename in self.filenames:
            rows = self.parser.parse(filename.full_path)
            for line_num, row in enumerate(rows, start=1):
                try:
                    record = self.builder.build(row, filename, line_num)
                    maybe_error = record.clean(self.cleaner)
                    if maybe_error:
                        self._errors.append(maybe_error)
                    yield record
                except FileParseException as e:
                    self._errors.append(e)

    def batch(self, batch_size: int, labeled_examples: Type[LabeledExamples]) -> Iterator[LabeledExamples]:
        batch = []
        for record in self:
            batch.append(record)
            if len(batch) == batch_size:
                yield labeled_examples(batch)
                batch = []
        if batch:
            yield labeled_examples(batch)

    @property
    def errors(self) -> List[FileParseException]:
        """Aggregates parser and builder errors."""
        errors = self.parser.errors + self._errors
        errors.sort(key=lambda error: error.line_num)
        return [error.dict() for error in errors]
