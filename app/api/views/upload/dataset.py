import csv
import json
from itertools import chain
from typing import Dict, Iterator, List, Optional, Type

import pyexcel

from .data import BaseData
from .label import Label
from .labels import Labels


class Record:

    def __init__(self,
                 data: Type[BaseData],
                 label: List[Label] = None):
        if label is None:
            label = []
        self._data = data
        self._label = label

    def __str__(self):
        return f'{self._data}\t{self._label}'

    @property
    def data(self):
        return self._data

    @property
    def annotation(self):
        return Labels(self._label)

    @property
    def label(self):
        return [label.name for label in self._label if label.has_name() and label.name]


class Records:

    def __init__(self, records: List[Record]):
        self.records = records

    def data(self):
        return [r.data.dict() for r in self.records]

    def annotation(self, mapping: Dict[str, int]):
        return [r.annotation.replace_label(mapping).dict() for r in self.records]

    def label(self):
        labels = set(chain(*[r.label for r in self.records]))
        return [
            {'text': label} for label in labels
        ]


class Dataset:

    def __init__(self,
                 filenames: List[str],
                 data_class: Type[BaseData],
                 label_class: Type[Label],
                 encoding: Optional[str] = None,
                 **kwargs):
        self.filenames = filenames
        self.data_class = data_class
        self.label_class = label_class
        self.encoding = encoding
        self.kwargs = kwargs

    def __iter__(self) -> Iterator[Record]:
        for filename in self.filenames:
            yield from self.load(filename)

    def batch(self, batch_size) -> Records:
        records = []
        for record in self:
            records.append(record)
            if len(records) == batch_size:
                yield Records(records)
                records = []
        yield Records(records)

    def load(self, filename: str) -> Iterator[Record]:
        """Loads a file content."""
        with open(filename, encoding=self.encoding) as f:
            data = self.data_class.parse(filename=filename, text=f.read())
            record = Record(data=data)
            yield record

    def from_row(self, filename: str, row: Dict) -> Record:
        text = row.pop(self.kwargs.get('column_data', 'text'))
        label = row.pop(self.kwargs.get('column_label', 'label'), [])
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
