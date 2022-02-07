import abc
from logging import getLogger
from typing import Any, Dict, List, Optional, Type

from pydantic import ValidationError

from .data import BaseData
from .exceptions import FileParseException
from .labels import Label
from .readers import Builder, Record

logger = getLogger(__name__)


class PlainBuilder(Builder):
    def __init__(self, data_class: Type[BaseData]):
        self.data_class = data_class

    def build(self, row: Dict[Any, Any], filename: str, line_num: int) -> Record:
        data = self.data_class.parse(filename=filename)
        return Record(data=data)


def build_label(row: Dict[Any, Any], name: str, label_class: Type[Label]) -> List[Label]:
    labels = row[name]
    labels = [labels] if isinstance(labels, (str, int)) else labels
    return [label_class.parse(label) for label in labels]


def build_data(row: Dict[Any, Any], name: str, data_class: Type[BaseData], filename: str) -> BaseData:
    data = row[name]
    return data_class.parse(text=data, filename=filename)


class Column(abc.ABC):
    # Todo: need to redesign.
    def __init__(self, name: str, value_class: Any):
        self.name = name
        self.value_class = value_class

    @abc.abstractmethod
    def __call__(self, row: Dict[Any, Any], filename: str):
        raise NotImplementedError("Please implement this method in the subclass.")


class DataColumn(Column):
    def __call__(self, row: Dict[Any, Any], filename: str) -> BaseData:
        return build_data(row, self.name, self.value_class, filename)


class LabelColumn(Column):
    def __call__(self, row: Dict[Any, Any], filename: str) -> List[Label]:
        return build_label(row, self.name, self.value_class)


class ColumnBuilder(Builder):
    def __init__(self, data_column: Column, label_columns: Optional[List[Column]] = None):
        self.data_column = data_column
        self.label_columns = label_columns or []

    def build(self, row: Dict[Any, Any], filename: str, line_num: int) -> Record:
        try:
            data = self.data_column(row, filename)
            row.pop(self.data_column.name)
        except KeyError:
            message = f"{self.data_column.name} field does not exist."
            raise FileParseException(filename, line_num, message)
        except ValidationError:
            message = "The empty text is not allowed."
            raise FileParseException(filename, line_num, message)

        labels = []
        for column in self.label_columns:
            try:
                labels.extend(column(row, filename))
                row.pop(column.name)
            except (KeyError, ValidationError, TypeError) as e:
                logger.error("Filename: %s, Line: %s, Data: %s, Error: %s" % (filename, line_num, row, str(e)))

        return Record(data=data, label=labels, line_num=line_num, meta=row)
