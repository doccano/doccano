import abc
import collections.abc
from typing import Any, Dict, Iterator, List, Type

from .cleaners import Cleaner
from .data import BaseData
from .exceptions import FileParseException
from .labels import Label

DEFAULT_TEXT_COLUMN = "text"
DEFAULT_LABEL_COLUMN = "label"


class Record:
    """Record represents a data."""

    def __init__(
        self, data: Type[BaseData], label: List[Label] = None, meta: Dict[Any, Any] = None, line_num: int = -1
    ):
        if label is None:
            label = []
        if meta is None:
            meta = {}
        self._data = data
        self._label = label
        self._meta = meta
        self._line_num = line_num

    def __str__(self):
        return f"{self._data}\t{self._label}"

    def clean(self, cleaner: Cleaner):
        label = cleaner.clean(self._label)
        changed = len(label) != len(self.label)
        self._label = label
        if changed:
            raise FileParseException(filename=self._data.filename, line_num=self._line_num, message=cleaner.message)

    @property
    def data(self):
        return self._data

    def create_data(self, project):
        return self._data.create(project, self._meta)

    def create_label(self, project):
        return [label.create(project) for label in self._label]

    def create_annotation(self, user, example, mapping):
        return [label.create_annotation(user, example, mapping) for label in self._label]

    @property
    def label(self):
        return [label.dict() for label in self._label if label.has_name() and label.name]


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


class Builder(abc.ABC):
    """The abstract Record builder."""

    @abc.abstractmethod
    def build(self, row: Dict[Any, Any], filename: str, line_num: int) -> Record:
        """Builds the record from the dictionary."""
        raise NotImplementedError("Please implement this method in the subclass.")


class Reader(BaseReader):
    def __init__(self, filenames: List[str], parser: Parser, builder: Builder):
        self.filenames = filenames
        self.parser = parser
        self.builder = builder
        self._errors: List[FileParseException] = []

    def __iter__(self) -> Iterator[Record]:
        for filename in self.filenames:
            rows = self.parser.parse(filename)
            for line_num, row in enumerate(rows, start=1):
                try:
                    yield self.builder.build(row, filename, line_num)
                except FileParseException as e:
                    self._errors.append(e)

    @property
    def errors(self) -> List[FileParseException]:
        """Aggregates parser and builder errors."""
        errors = self.parser.errors + self._errors
        return errors
