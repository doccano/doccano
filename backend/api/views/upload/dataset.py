import csv
import io
import json
import os
from typing import Dict, Iterator, List, Optional, Type

import chardet
import pydantic.error_wrappers
import pyexcel
from chardet.universaldetector import UniversalDetector
from seqeval.scheme import BILOU, IOB2, IOBES, IOE2, Tokens

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
            try:
                yield from self.load(filename)
            except UnicodeDecodeError as err:
                message = str(err)
                raise FileParseException(filename, line_num=-1, message=message)

    def load(self, filename: str) -> Iterator[Record]:
        """Loads a file content."""
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
            data = self.data_class.parse(filename=filename, text=f.read())
            record = Record(data=data)
            yield record

    def detect_encoding(self, filename: str, buffer_size=io.DEFAULT_BUFFER_SIZE):
        if self.encoding != 'Auto':
            return self.encoding

        # For a small file.
        if os.path.getsize(filename) < buffer_size:
            detected = chardet.detect(open(filename, 'rb').read())
            return detected.get('encoding', 'utf-8')

        # For a large file.
        with open(filename, 'rb') as f:
            detector = UniversalDetector()
            while True:
                binary = f.read(buffer_size)
                detector.feed(binary)
                if binary == b'':
                    break
                if detector.done:
                    break
            if detector.done:
                return detector.result['encoding']
            else:
                return 'utf-8'

    def from_row(self, filename: str, row: Dict, line_num: int) -> Record:
        column_data = self.kwargs.get('column_data', 'text')
        if column_data not in row:
            message = f'{column_data} does not exist.'
            raise FileParseException(filename, line_num, message)
        text = row.pop(column_data)
        label = row.pop(self.kwargs.get('column_label', 'label'), [])
        label = [label] if isinstance(label, str) else label
        try:
            label = [self.label_class.parse(o) for o in label]
        except pydantic.error_wrappers.ValidationError:
            label = []
        data = self.data_class.parse(text=text, filename=filename, meta=row)
        record = Record(data=data, label=label)
        return record


class FileBaseDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        data = self.data_class.parse(filename=filename)
        record = Record(data=data)
        yield record


class TextFileDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
            data = self.data_class.parse(filename=filename, text=f.read())
            record = Record(data=data)
            yield record


class TextLineDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
            for line in f:
                data = self.data_class.parse(filename=filename, text=line.rstrip())
                record = Record(data=data)
                yield record


class CsvDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
            delimiter = self.kwargs.get('delimiter', ',')
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader)

            column_data = self.kwargs.get('column_data', 'text')
            if column_data not in header:
                message = f'Column `{column_data}` does not exist in the header: {header}'
                raise FileParseException(filename, 1, message)

            for line_num, row in enumerate(reader, start=2):
                row = dict(zip(header, row))
                yield self.from_row(filename, row, line_num)


class JSONDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
            dataset = json.load(f)
            for line_num, row in enumerate(dataset, start=1):
                yield self.from_row(filename, row, line_num)


class JSONLDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
            for line_num, line in enumerate(f, start=1):
                row = json.loads(line)
                yield self.from_row(filename, row, line_num)


class ExcelDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        records = pyexcel.iget_records(file_name=filename)
        for line_num, row in enumerate(records, start=1):
            yield self.from_row(filename, row, line_num)


class FastTextDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
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


class CoNLLDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        encoding = self.detect_encoding(filename)
        with open(filename, encoding=encoding) as f:
            words, tags = [], []
            delimiter = self.kwargs.get('delimiter', ' ')
            for line_num, line in enumerate(f, start=1):
                line = line.rstrip()
                if line:
                    tokens = line.split('\t')
                    if len(tokens) != 2:
                        message = 'A line must be separated by tab and has two columns.'
                        raise FileParseException(filename, line_num, message)
                    word, tag = tokens
                    words.append(word)
                    tags.append(tag)
                else:
                    text = delimiter.join(words)
                    data = self.data_class.parse(filename=filename, text=text)
                    labels = self.get_label(words, tags, delimiter)
                    record = Record(data=data, label=labels)
                    yield record
                    words, tags = [], []

    def get_scheme(self, scheme: str):
        mapping = {
            'IOB2': IOB2,
            'IOE2': IOE2,
            'IOBES': IOBES,
            'BILOU': BILOU
        }
        return mapping[scheme]

    def get_label(self, words: List[str], tags: List[str], delimiter: str) -> List[Label]:
        scheme = self.get_scheme(self.kwargs.get('scheme', 'IOB2'))
        tokens = Tokens(tags, scheme)
        labels = []
        for entity in tokens.entities:
            text = delimiter.join(words[:entity.start])
            start = len(text) + len(delimiter) if text else len(text)
            chunk = words[entity.start: entity.end]
            text = delimiter.join(chunk)
            end = start + len(text)
            labels.append(self.label_class.parse((start, end, entity.tag)))
        return labels
