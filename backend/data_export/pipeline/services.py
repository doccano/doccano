from typing import List

from .dataset import Dataset
from .formatters import Formatter
from .writers import Writer


class ExportApplicationService:
    def __init__(self, dataset: Dataset, formatters: List[Formatter], writer: Writer):
        self.dataset = dataset
        self.formatters = formatters
        self.writer = writer

    def export(self, file):
        dataset = self.dataset.to_dataframe()
        for formatter in self.formatters:
            dataset = formatter.format(dataset)
        self.writer.write(file, dataset)
        return file
