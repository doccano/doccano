import abc
import collections.abc
import dataclasses
import uuid
from typing import Any, Dict, Iterator, List

import pandas as pd

from .exceptions import FileParseException

DEFAULT_TEXT_COLUMN = "text"
DEFAULT_LABEL_COLUMN = "label"
FILE_NAME_COLUMN = "filename"
UPLOAD_NAME_COLUMN = "upload_name"
UUID_COLUMN = "example_uuid"
LINE_NUMBER_COLUMN = "#line_number"


class BaseReader(collections.abc.Iterable):
    """Reader has a role to parse files and return a Record iterator."""

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Dict[Any, Any]]:
        """Creates an iterator for elements of this dataset.

        Returns:
            A `dict` for the elements of this dataset.
        """
        raise NotImplementedError("Please implement this method in the subclass.")

    @property
    @abc.abstractmethod
    def errors(self):
        raise NotImplementedError("Please implement this method in the subclass.")

    @abc.abstractmethod
    def batch(self, batch_size: int) -> Iterator[pd.DataFrame]:
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


class Reader(BaseReader):
    def __init__(self, filenames: List[FileName], parser: Parser):
        self.filenames = filenames
        self.parser = parser

    def __iter__(self) -> Iterator[Dict[Any, Any]]:
        for filename in self.filenames:
            rows = self.parser.parse(filename.full_path)
            for row in rows:
                yield {
                    UUID_COLUMN: uuid.uuid4(),
                    FILE_NAME_COLUMN: filename.generated_name,
                    UPLOAD_NAME_COLUMN: filename.upload_name,
                    **row,
                }

    def batch(self, batch_size: int) -> Iterator[pd.DataFrame]:
        batch = []
        for record in self:
            batch.append(record)
            if len(batch) == batch_size:
                yield pd.DataFrame(batch)
                batch = []
        if batch:
            yield pd.DataFrame(batch)

    @property
    def errors(self) -> List[FileParseException]:
        return self.parser.errors
