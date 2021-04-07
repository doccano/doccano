import csv
import json
from typing import Dict, Iterator, List, Optional, Type

import pyexcel

from .data import BaseData
from .exception import FileParseException
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
        return self._data.dict()

    def annotation(self, mapping: Dict[str, int]):
        labels = Labels(self._label)
        labels = labels.replace_label(mapping)
        return labels.dict()

    @property
    def label(self):
        return [
            {
                'text': label.name
            } for label in self._label
            if label.has_name() and label.name
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

    def load(self, filename: str) -> Iterator[Record]:
        """Loads a file content."""
        with open(filename, encoding=self.encoding) as f:
            data = self.data_class.parse(filename=filename, text=f.read())
            record = Record(data=data)
            yield record

    def from_row(self, filename: str, row: Dict, line_num: int) -> Record:
        column_data = self.kwargs.get('column_data', 'text')
        if column_data not in row:
            message = f'{column_data} does not exist.'
            raise FileParseException(filename, line_num, message)
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

            column_data = self.kwargs.get('column_data', 'text')
            if column_data not in header:
                message = f'{column_data} does not exist in the header: {header}'
                raise FileParseException(filename, 1, message)

            for line_num, row in enumerate(reader, start=2):
                row = dict(zip(header, row))
                yield self.from_row(filename, row, line_num)


class JSONDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            dataset = json.load(f)
            for line_num, row in enumerate(dataset, start=1):
                yield self.from_row(filename, row, line_num)


class JSONLDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            for line_num, line in enumerate(f, start=1):
                row = json.loads(line)
                yield self.from_row(filename, row, line_num)


class ExcelDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        records = pyexcel.iget_records(filename)
        for line_num, row in enumerate(records, start=1):
            yield self.from_row(filename, row, line_num)


class FastTextDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename, encoding=self.encoding) as f:
            for line_num, line in enumerate(f, start=1):
                labels = []
                tokens = []
                for token in line.rstrip().split(' '):
                    if token.startswith('__label__'):
                        if token == '__label__':
                            message = 'Label name is empty.'
                            raise FileParseException(filename, line_num, message)
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
