import csv
import json
from typing import Dict, Iterator, List, Optional, Type

import pyexcel

from .data import BaseData
from .label import Label


class Record:

    def __init__(self,
                 data: Type[BaseData],
                 label: List[Label] = None):
        if label is None:
            label = []
        self.data = data
        self.label = label

    def __str__(self):
        return f'{self.data}\t{self.label}'


class Dataset:

    def __init__(self,
                 filenames: List[str],
                 data_class: Type[BaseData],
                 label_class: Type[Label],
                 encoding: Optional[str] = None,
                 column_data: str = 'text',
                 column_label: str = 'label',
                 **kwargs):
        self.filenames = filenames
        self.data_class = data_class
        self.label_class = label_class
        self.encoding = encoding
        self.column_data = column_data
        self.column_label = column_label
        self.kwargs = kwargs

    def __iter__(self) -> Iterator[Record]:
        for filename in self.filenames:
            yield from self.load(filename)

    def load(self, filename: str) -> Iterator[Record]:
        """Loads a file content."""
        with open(filename, encoding=self.encoding) as f:
            data = self.data_class.parse(filename=filename, text=f.read())
            record = Record(data=data)
            yield record

    def from_row(self, filename: str, row: Dict) -> Record:
        text = row.pop(self.column_data)
        label = row.pop(self.column_label, [])
        label = [label] if isinstance(label, str) else label
        label = [self.label_class.parse(o) for o in label]
        data = self.data_class.parse(text=text, filename=filename, metadata=row)
        record = Record(data=data, label=label)
        return record


class FileBaseDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        data = self.data_class.parse(filename=filename)
        record = Record(data=data)
        yield record


class TextFileDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            data = self.data_class.parse(filename=filename, text=f.read())
            record = Record(data=data)
            yield record


class TextLineDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            for line in f:
                data = self.data_class.parse(filename=filename, text=line.rstrip())
                record = Record(data=data)
                yield record


class CsvDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            delimiter = self.kwargs.get('delimiter', ',')
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader)
            for row in reader:
                row = dict(zip(header, row))
                yield self.from_row(filename, row)


class JSONDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            dataset = json.load(f)
            for row in dataset:
                yield self.from_row(filename, row)


class JSONLDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            for line in f:
                row = json.loads(line)
                yield self.from_row(filename, row)


class ExcelDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        records = pyexcel.iget_records(filename)
        for row in records:
            yield self.from_row(filename, row)


class FastTextDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            for i, line in enumerate(f, start=1):
                labels = []
                tokens = []
                for token in line.rstrip().split(' '):
                    if token.startswith('__label__'):
                        label_name = token[len('__label__'):]
                        labels.append(self.label_class.parse(label_name))
                    else:
                        tokens.append(token)
                text = ' '.join(tokens)
                data = self.data_class.parse(filename=filename, text=text)
                record = Record(data=data, label=labels)
                yield record


class ConllDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            pass
