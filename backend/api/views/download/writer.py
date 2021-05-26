import abc
import csv
import itertools
import json
import os
import uuid
import zipfile
from collections import defaultdict
from typing import Dict, Iterable, Iterator, List

from .data import Record


class BaseWriter:

    def __init__(self, tmpdir: str):
        self.tmpdir = tmpdir

    @abc.abstractmethod
    def write(self, records: Iterator[Record]) -> str:
        raise NotImplementedError()

    def write_zip(self, filenames: Iterable):
        save_file = '{}.zip'.format(os.path.join(self.tmpdir, str(uuid.uuid4())))
        with zipfile.ZipFile(save_file, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for file in filenames:
                zf.write(filename=file, arcname=os.path.basename(file))
        return save_file


class LineWriter(BaseWriter):
    extension = 'txt'

    def write(self, records: Iterator[Record]) -> str:
        files = {}
        for record in records:
            filename = os.path.join(self.tmpdir, f'{record.user}.{self.extension}')
            if filename not in files:
                f = open(filename, mode='a')
                files[filename] = f
            f = files[filename]
            line = self.create_line(record)
            f.write(f'{line}\n')
        for f in files.values():
            f.close()
        save_file = self.write_zip(files)
        for file in files:
            os.remove(file)
        return save_file

    @abc.abstractmethod
    def create_line(self, record) -> str:
        raise NotImplementedError()


class CsvWriter(BaseWriter):
    extension = 'csv'

    def write(self, records: Iterator[Record]) -> str:
        writers = {}
        file_handlers = set()
        records = list(records)
        header = self.create_header(records)
        for record in records:
            filename = os.path.join(self.tmpdir, f'{record.user}.{self.extension}')
            if filename not in writers:
                f = open(filename, mode='a', encoding='utf-8')
                writer = csv.DictWriter(f, header)
                writer.writeheader()
                writers[filename] = writer
                file_handlers.add(f)
            writer = writers[filename]
            line = self.create_line(record)
            writer.writerow(line)

        for f in file_handlers:
            f.close()
        save_file = self.write_zip(writers)
        for file in writers:
            os.remove(file)
        return save_file

    def create_line(self, record) -> Dict:
        return {
            'id': record.id,
            'data': record.data,
            'label': '#'.join(record.label),
            **record.metadata
        }

    def create_header(self, records: List[Record]) -> Iterable[str]:
        header = ['id', 'data', 'label']
        header += list(itertools.chain(*[r.metadata.keys() for r in records]))
        return header


class JSONWriter(BaseWriter):
    extension = 'json'

    def write(self, records: Iterator[Record]) -> str:
        writers = {}
        contents = defaultdict(list)
        for record in records:
            filename = os.path.join(self.tmpdir, f'{record.user}.{self.extension}')
            if filename not in writers:
                f = open(filename, mode='a', encoding='utf-8')
                writers[filename] = f
            line = self.create_line(record)
            contents[filename].append(line)

        for filename, f in writers.items():
            content = contents[filename]
            json.dump(content, f, ensure_ascii=False)
            f.close()

        save_file = self.write_zip(writers)
        for file in writers:
            os.remove(file)
        return save_file

    def create_line(self, record) -> Dict:
        return {
            'id': record.id,
            'data': record.data,
            'label': record.label,
            **record.metadata
        }


class JSONLWriter(LineWriter):
    extension = 'jsonl'

    def create_line(self, record):
        return json.dumps({
            'id': record.id,
            'data': record.data,
            'label': record.label,
            **record.metadata
        }, ensure_ascii=False)


class FastTextWriter(LineWriter):
    extension = 'txt'

    def create_line(self, record):
        line = [f'__label__{label}' for label in record.label]
        line.append(record.data)
        line = ' '.join(line)
        return line
