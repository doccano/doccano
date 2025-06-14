from typing import List, Optional, Type

import pandas as pd

from .data import BaseData
from .exceptions import FileParseException
from .label import Label
from .readers import (
    DEFAULT_TEXT_COLUMN,
    LINE_NUMBER_COLUMN,
    UPLOAD_NAME_COLUMN,
    UUID_COLUMN,
)
from examples.models import Example
from projects.models import Project


class ExampleMaker:
    def __init__(
        self,
        project: Project,
        data_class: Type[BaseData],
        column_data: str = DEFAULT_TEXT_COLUMN,
        exclude_columns: Optional[List[str]] = None,
    ):
        self.project = project
        self.data_class = data_class
        self.column_data = column_data
        self.exclude_columns = exclude_columns or []
        self._errors: List[FileParseException] = []

    def make(self, df: pd.DataFrame) -> List[Example]:
        if not self.check_column_existence(df):
            return []
        self.check_value_existence(df)
        # make dataframe without exclude columns and missing data
        df_with_data_column = df.loc[:, ~df.columns.isin(self.exclude_columns)]
        df_with_data_column = df_with_data_column.dropna(subset=[self.column_data])

        examples = []
        for row in df_with_data_column.to_dict(orient="records"):
            line_num = row.pop(LINE_NUMBER_COLUMN, 0)
            row[DEFAULT_TEXT_COLUMN] = row.pop(self.column_data)  # Rename column for parsing
            try:
                data = self.data_class.parse(**row)
                example = data.create(self.project)
                examples.append(example)
            except ValueError:
                message = f"Invalid data in line {line_num}"
                error = FileParseException(row[UPLOAD_NAME_COLUMN], line_num, message)
                self._errors.append(error)
        return examples

    def check_column_existence(self, df: pd.DataFrame) -> bool:
        message = f"Column {self.column_data} not found in the file"
        if self.column_data not in df.columns:
            for filename in df[UPLOAD_NAME_COLUMN].unique():
                self._errors.append(FileParseException(filename, 0, message))
            return False
        return True

    def check_value_existence(self, df: pd.DataFrame):
        df_without_data_column = df[df[self.column_data].isnull()]
        for row in df_without_data_column.to_dict(orient="records"):
            message = f"Column {self.column_data} not found in record"
            error = FileParseException(row[UPLOAD_NAME_COLUMN], row.get(LINE_NUMBER_COLUMN, 0), message)
            self._errors.append(error)

    @property
    def errors(self) -> List[FileParseException]:
        self._errors.sort(key=lambda error: error.line_num)
        return self._errors


class BinaryExampleMaker(ExampleMaker):
    def make(self, df: pd.DataFrame) -> List[Example]:
        examples = []
        for row in df.to_dict(orient="records"):
            data = self.data_class.parse(**row)
            example = data.create(self.project)
            examples.append(example)
        return examples


class LabelMaker:
    def __init__(self, column: str, label_class: Type[Label]):
        self.column = column
        self.label_class = label_class
        self._errors: List[FileParseException] = []

    def make(self, df: pd.DataFrame) -> List[Label]:
        if not self.check_column_existence(df):
            return []

        df_label = df.explode(self.column)
        df_label = df_label[[UUID_COLUMN, self.column]]
        df_label.dropna(subset=[self.column], inplace=True)
        labels = []
        for row in df_label.to_dict(orient="records"):
            try:
                label = self.label_class.parse(row[UUID_COLUMN], row[self.column])
                labels.append(label)
            except ValueError:
                pass
        return labels

    def check_column_existence(self, df: pd.DataFrame) -> bool:
        message = f"Column {self.column} not found in the file"
        if self.column not in df.columns:
            for filename in df[UPLOAD_NAME_COLUMN].unique():
                self._errors.append(FileParseException(filename, 0, message))
            return False
        return True

    @property
    def errors(self) -> List[FileParseException]:
        self._errors.sort(key=lambda error: error.line_num)
        return self._errors
