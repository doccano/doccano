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
        """Format the label column to `LabelA#LabelB` format."""
        if self.target_column not in dataset.columns:
            return dataset

        dataset[self.target_column] = dataset[self.target_column].apply(
            lambda labels: "#".join(sorted(label.to_string() for label in labels))
        )
        return dataset


class ListedCategoryFormatter(Formatter):
    def format(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Format the label column to `['LabelA', 'LabelB']` format."""
        if self.target_column not in dataset.columns:
            return dataset

        dataset[self.target_column] = dataset[self.target_column].apply(
            lambda labels: sorted([label.to_string() for label in labels])
        )
        return dataset


class FastTextCategoryFormatter(Formatter):
    def format(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """Format the label column to `__label__LabelA __label__LabelB` format.
        Also, drop the columns except for `data` and `self.target_column`.
        """
        if self.target_column not in dataset.columns:
            return dataset

        dataset = dataset[["data", self.target_column]]
        dataset[self.target_column] = dataset[self.target_column].apply(
            lambda labels: sorted(f"__label__{label.to_string()}" for label in labels)
        )
        return dataset
