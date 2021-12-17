import abc
import collections.abc
from typing import Any, Dict, Iterator, List, Type

from .data import BaseData
from .label import Label

DEFAULT_TEXT_COLUMN = 'text'
DEFAULT_LABEL_COLUMN = 'labels'


class Record:

    def __init__(self,
                 data: Type[BaseData],
                 label: List[Label] = None,
                 meta: Dict[Any, Any] = None,
                 line_num: int = -1):
        if label is None:
            label = []
        if meta is None:
            meta = {}
        self._data = data
        self._label = label
        self._meta = meta
        self._line_num = line_num

    def __str__(self):
        return f'{self._data}\t{self._label}'

    @property
    def data(self):
        return self._data.dict()

    @property
    def label(self):
        return [
            {
                'text': label.name
            } for label in self._label
            if label.has_name() and label.name
        ]


class BaseReader(collections.abc.Iterable):

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Record]:
        """Creates an iterator for elements of this dataset.

        Returns:
            A `Record` for the elements of this dataset.
        """
        raise NotImplementedError('Please implement this method in the subclass.')

    @property
    @abc.abstractmethod
    def errors(self):
        raise NotImplementedError('Please implement this method in the subclass.')


class Parser(abc.ABC):

    @abc.abstractmethod
    def parse(self, filename: str) -> Iterator[Dict[Any, Any]]:
        """Parses the file and returns the dictionary."""
        raise NotImplementedError('Please implement this method in the subclass.')


class Builder(abc.ABC):

    @abc.abstractmethod
    def build(self, row: Dict[Any, Any], filename: str, line_num: int) -> Record:
        """Builds the record from the dictionary."""
        raise NotImplementedError('Please implement this method in the subclass.')


class Reader(BaseReader):

    def __init__(self, filenames: List[str], parser: Parser, builder: Builder):
        self.filenames = filenames
        self.parser = parser
        self.builder = builder
        self._errors = []

    def __iter__(self) -> Iterator[Record]:
        for filename in self.filenames:
            rows = self.parser.parse(filename)
            for line_num, row in enumerate(rows, start=1):
                record = self.builder.build(row, filename, line_num)
                yield record

    @property
    def errors(self):
        """Aggregates parser and builder errors."""
        return self._errors
