from typing import Type

import pandas as pd

from .data import BaseData
from .labels import Label
from .readers import LINE_NUM_COLUMN


class DataFormatter:
    def __init__(self, column: str, data_class: Type[BaseData]):
        self.column = column
        self.data_class = data_class

    def format(self, df: pd.DataFrame) -> pd.DataFrame:
        df_data = df[[LINE_NUM_COLUMN, self.column]]
        df_data.dropna(inplace=True)
        return df_data


class LabelFormatter:
    def __init__(self, column: str, label_class: Type[Label]):
        self.column = column
        self.label_class = label_class

    def format(self, df: pd.DataFrame) -> pd.DataFrame:
        df_label = df[[LINE_NUM_COLUMN, self.column]].explode(self.column)
        df_label.dropna(inplace=True)
        df_label[self.column] = df_label[self.column].map(self.label_class.parse)
        df_label.dropna(inplace=True)
        df_label.reset_index(inplace=True, drop=True)
        return df_label
