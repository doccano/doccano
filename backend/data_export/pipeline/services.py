from .dataset import Dataset
from .formatters import Formatter
from .writers import Writer


class ExportApplicationService:
    def __init__(self, dataset: Dataset, formatter: Formatter, writer: Writer):
        self.dataset = dataset
        self.formatter = formatter
        self.writer = writer

    def export(self, file):
        dataset = self.dataset.to_dataframe()
        dataset = self.formatter.format(dataset)
        self.writer.write(file, dataset)
        return file
