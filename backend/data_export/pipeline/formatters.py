"""
Convert a dataset to the specified format.
"""
import abc

import pandas as pd


class Formatter(abc.ABC):
    def __init__(self, target_column: str):
        self.target_column = target_column

    @abc.abstractmethod
    def format(self, dataset: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Please implement this method in the subclass.")


class JoinedCategoryFormatter(Formatter):
    def format(self, dataset: pd.DataFrame) -> pd.DataFrame:
        dataset[self.target_column] = dataset[self.target_column].apply(
            lambda labels: [label.to_string() for label in labels]
        )
        return dataset
