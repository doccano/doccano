from typing import Type

import pandas as pd

from .data import BaseData
from .labels import Label
from .readers import (
    DEFAULT_LABEL_COLUMN,
    DEFAULT_TEXT_COLUMN,
    LINE_NUM_COLUMN,
    UUID_COLUMN,
)

DEFAULT_DATA_COLUMN = "#data"


class DataFormatter:
    def __init__(self, column: str, data_class: Type[BaseData]):
        self.column = column
        self.data_class = data_class

    def format(self, df: pd.DataFrame) -> pd.DataFrame:
        df.drop(columns=[LINE_NUM_COLUMN], inplace=True)
        df.dropna(subset=[self.column], inplace=True)
        df.rename(columns={self.column: DEFAULT_TEXT_COLUMN}, inplace=True)
        df[DEFAULT_DATA_COLUMN] = df.apply(lambda row: self.data_class.parse(**row.to_dict()), axis=1)
        return df[[UUID_COLUMN, DEFAULT_DATA_COLUMN]]


class LabelFormatter:
    def __init__(self, column: str, label_class: Type[Label]):
        self.column = column
        self.label_class = label_class

    def format(self, df: pd.DataFrame) -> pd.DataFrame:
        df_label = df[[UUID_COLUMN, self.column]].explode(self.column)
        df_label.dropna(inplace=True)
        df_label[DEFAULT_LABEL_COLUMN] = df_label[self.column].map(self.label_class.parse)
        df_label.dropna(inplace=True)
        df_label.reset_index(inplace=True, drop=True)
        return df_label
