from typing import Any, Dict, Type

from pydantic import ValidationError

from .data import BaseData
from .exception import FileParseException
from .label import Label
from .readers import DEFAULT_LABEL_COLUMN, DEFAULT_TEXT_COLUMN, Builder, Record


class PlainBuilder(Builder):

    def __init__(self, data_class: Type[BaseData]):
        self.data_class = data_class

    def build(self, row: Dict[Any, Any], filename: str, line_num: int) -> Record:
        data = self.data_class.parse(filename=filename)
        yield Record(data=data)


class ColumnBuilder(Builder):

    def __init__(self,
                 data_class: Type[BaseData],
                 label_class: Type[Label],
                 text_column: str = DEFAULT_TEXT_COLUMN,
                 label_column: str = DEFAULT_LABEL_COLUMN):
        self.data_class = data_class
        self.label_class = label_class
        self.text_column = text_column
        self.label_column = label_column

    def build(self, row: Dict[Any, Any], filename: str, line_num: int) -> Record:
        if self.text_column not in row:
            message = f'{self.text_column} does not exist.'
            raise FileParseException(filename, line_num, message)
        text = row.pop(self.text_column)
        label = row.pop(self.label_column, [])
        label = [label] if isinstance(label, str) else label
        try:
            label = [self.label_class.parse(o) for o in label]
        except (ValidationError, TypeError):
            label = []

        try:
            data = self.data_class.parse(text=text, filename=filename, meta=row)
            return Record(data=data, label=label, line_num=line_num)
        except ValidationError:
            message = 'The empty text is not allowed.'
            raise FileParseException(filename, line_num, message)
