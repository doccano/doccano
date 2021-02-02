import base64
import csv
import io
import itertools
import json
import mimetypes
import re
from collections import defaultdict

import conllu
from chardet import UniversalDetector
from django.db import transaction
from django.conf import settings
from colour import Color
import pyexcel
from rest_framework.renderers import JSONRenderer, BaseRenderer
from seqeval.metrics.sequence_labeling import get_entities

from .exceptions import FileParseException
from .models import Label
from .serializers import DocumentSerializer, LabelSerializer


def extract_label(tag):
    ptn = re.compile(r'(B|I|E|S)-(.+)')
    m = ptn.match(tag)
    if m:
        return m.groups()[1]
    else:
        return tag


class BaseStorage(object):

    def __init__(self, data, project):
        self.data = data
        self.project = project

    @transaction.atomic
    def save(self, user):
        raise NotImplementedError()

    def save_doc(self, data):
        serializer = DocumentSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        doc = serializer.save(project=self.project)
        return doc

    def save_label(self, data):
        serializer = LabelSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        label = serializer.save(project=self.project)
        return label

    def save_annotation(self, data, user):
        annotation_serializer = self.project.get_annotation_serializer()
        serializer = annotation_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        annotation = serializer.save(user=user)
        return annotation

    @classmethod
    def extract_label(cls, data):
        return [d.get('labels', []) for d in data]

    @classmethod
    def exclude_created_labels(cls, labels, created):
        return [label for label in labels if label not in created]

    @classmethod
    def to_serializer_format(cls, labels, created):
        existing_shortkeys = {(label.suffix_key, label.prefix_key)
                              for label in created.values()}

        serializer_labels = []

        for label in sorted(labels):
            serializer_label = {'text': label}

            shortkey = cls.get_shortkey(label, existing_shortkeys)
            if shortkey:
                serializer_label['suffix_key'] = shortkey[0]
                serializer_label['prefix_key'] = shortkey[1]
                existing_shortkeys.add(shortkey)

            background_color = Color(pick_for=label)
            text_color = Color('white') if background_color.get_luminance() < 0.5 else Color('black')
            serializer_label['background_color'] = background_color.hex
            serializer_label['text_color'] = text_color.hex

            serializer_labels.append(serializer_label)

        return serializer_labels

    @classmethod
    def get_shortkey(cls, label, existing_shortkeys):
        model_prefix_keys = [key for (key, _) in Label.PREFIX_KEYS]
        prefix_keys = [None] + model_prefix_keys

        model_suffix_keys = {key for (key, _) in Label.SUFFIX_KEYS}
        suffix_keys = [key for key in label.lower() if key in model_suffix_keys]

        for shortkey in itertools.product(suffix_keys, prefix_keys):
            if shortkey not in existing_shortkeys:
                return shortkey

        return None

    @classmethod
    def update_saved_labels(cls, saved, new):
        for label in new:
            saved[label.text] = label
        return saved


class PlainStorage(BaseStorage):

    @transaction.atomic
    def save(self, user):
        for text in self.data:
            self.save_doc(text)


class ClassificationStorage(BaseStorage):
    """Store json for text classification.

    The format is as follows:
    {"text": "Python is awesome!", "labels": ["positive"]}
    ...
    """
    @transaction.atomic
    def save(self, user):
        saved_labels = {label.text: label for label in self.project.labels.all()}
        for data in self.data:
            docs = self.save_doc(data)
            labels = self.extract_label(data)
            unique_labels = self.extract_unique_labels(labels)
            unique_labels = self.exclude_created_labels(unique_labels, saved_labels)
            unique_labels = self.to_serializer_format(unique_labels, saved_labels)
            new_labels = self.save_label(unique_labels)
            saved_labels = self.update_saved_labels(saved_labels, new_labels)
            annotations = self.make_annotations(docs, labels, saved_labels)
            self.save_annotation(annotations, user)

    @classmethod
    def extract_unique_labels(cls, labels):
        return set(itertools.chain(*labels))

    @classmethod
    def make_annotations(cls, docs, labels, saved_labels):
        annotations = []
        for doc, label in zip(docs, labels):
            for name in label:
                label = saved_labels[name]
                annotations.append({'document': doc.id, 'label': label.id})
        return annotations


class SequenceLabelingStorage(BaseStorage):
    """Upload jsonl for sequence labeling.

    The format is as follows:
    {"text": "Python is awesome!", "labels": [[0, 6, "Product"],]}
    ...
    """
    @transaction.atomic
    def save(self, user):
        saved_labels = {label.text: label for label in self.project.labels.all()}
        for data in self.data:
            docs = self.save_doc(data)
            labels = self.extract_label(data)
            unique_labels = self.extract_unique_labels(labels)
            unique_labels = self.exclude_created_labels(unique_labels, saved_labels)
            unique_labels = self.to_serializer_format(unique_labels, saved_labels)
            new_labels = self.save_label(unique_labels)
            saved_labels = self.update_saved_labels(saved_labels, new_labels)
            annotations = self.make_annotations(docs, labels, saved_labels)
            self.save_annotation(annotations, user)

    @classmethod
    def extract_unique_labels(cls, labels):
        return set([label for _, _, label in itertools.chain(*labels)])

    @classmethod
    def make_annotations(cls, docs, labels, saved_labels):
        annotations = []
        for doc, spans in zip(docs, labels):
            for span in spans:
                start_offset, end_offset, name = span
                label = saved_labels[name]
                annotations.append({'document': doc.id,
                                    'label': label.id,
                                    'start_offset': start_offset,
                                    'end_offset': end_offset})
        return annotations


class Seq2seqStorage(BaseStorage):
    """Store json for seq2seq.

    The format is as follows:
    {"text": "Hello, World!", "labels": ["こんにちは、世界!"]}
    ...
    """
    @transaction.atomic
    def save(self, user):
        for data in self.data:
            doc = self.save_doc(data)
            labels = self.extract_label(data)
            annotations = self.make_annotations(doc, labels)
            self.save_annotation(annotations, user)

    @classmethod
    def make_annotations(cls, docs, labels):
        annotations = []
        for doc, texts in zip(docs, labels):
            for text in texts:
                annotations.append({'document': doc.id, 'text': text})
        return annotations


class Speech2textStorage(BaseStorage):
    """Store json for speech2text.

    The format is as follows:
    {"audio": "data:audio/mpeg;base64,...", "transcription": "こんにちは、世界!"}
    ...
    """
    @transaction.atomic
    def save(self, user):
        for data in self.data:
            for audio in data:
                audio['text'] = audio.pop('audio')
            doc = self.save_doc(data)
            annotations = self.make_annotations(doc, data)
            self.save_annotation(annotations, user)

    @classmethod
    def make_annotations(cls, docs, data):
        annotations = []
        for doc, datum in zip(docs, data):
            try:
                annotations.append({'document': doc.id, 'text': datum['transcription']})
            except KeyError:
                continue
        return annotations


class FileParser(object):

    def parse(self, file):
        raise NotImplementedError()

    @staticmethod
    def encode_metadata(data):
        return json.dumps(data, ensure_ascii=False)


class CoNLLParser(FileParser):
    """Uploads CoNLL format file.

    The file format is tab-separated values.
    A blank line is required at the end of a sentence.
    For example:
    ```
    EU	B-ORG
    rejects	O
    German	B-MISC
    call	O
    to	O
    boycott	O
    British	B-MISC
    lamb	O
    .	O

    Peter	B-PER
    Blackburn	I-PER
    ...
    ```
    """
    def parse(self, file):
        data = []
        file = EncodedIO(file)
        file = io.TextIOWrapper(file, encoding=file.encoding)

        # Add check exception

        field_parsers = {
            "ne": lambda line, i: conllu.parser.parse_nullable_value(line[i]),
        }

        gen_parser = conllu.parse_incr(
            file,
            fields=("form", "ne"),
            field_parsers=field_parsers
        )

        try:
            for sentence in gen_parser:
                if not sentence:
                    continue
                if len(data) >= settings.IMPORT_BATCH_SIZE:
                    yield data
                    data = []
                words, labels = [], []
                for item in sentence:
                    word = item.get("form")
                    tag = item.get("ne")

                    if tag is not None:
                        char_left = sum(map(len, words)) + len(words)
                        char_right = char_left + len(word)
                        span = [char_left, char_right, tag]
                        labels.append(span)

                    words.append(word)

                # Create and add JSONL
                data.append({'text': ' '.join(words), 'labels': labels})

        except conllu.parser.ParseException as e:
            raise FileParseException(line_num=-1, line=str(e))

        if data:
            yield data


class PlainTextParser(FileParser):
    """Uploads plain text.

    The file format is as follows:
    ```
    EU rejects German call to boycott British lamb.
    President Obama is speaking at the White House.
    ...
    ```
    """
    def parse(self, file):
        file = EncodedIO(file)
        file = io.TextIOWrapper(file, encoding=file.encoding)
        while True:
            batch = list(itertools.islice(file, settings.IMPORT_BATCH_SIZE))
            if not batch:
                break
            yield [{'text': line.strip()} for line in batch]


class CSVParser(FileParser):
    """Uploads csv file.

    The file format is comma separated values.
    Column names are required at the top of a file.
    For example:
    ```
    text, label
    "EU rejects German call to boycott British lamb.",Politics
    "President Obama is speaking at the White House.",Politics
    "He lives in Newark, Ohio.",Other
    ...
    ```
    """
    def parse(self, file):
        file = EncodedIO(file)
        file = io.TextIOWrapper(file, encoding=file.encoding)
        reader = csv.reader(file)
        yield from ExcelParser.parse_excel_csv_reader(reader)


class ExcelParser(FileParser):
    def parse(self, file):
        excel_book = pyexcel.iget_book(file_type="xlsx", file_content=file.read())
        # Handle multiple sheets
        for sheet_name in excel_book.sheet_names():
            reader = excel_book[sheet_name].to_array()
            yield from self.parse_excel_csv_reader(reader)

    @staticmethod
    def parse_excel_csv_reader(reader):
        columns = next(reader)
        data = []
        if len(columns) == 1 and columns[0] != 'text':
            data.append({'text': columns[0]})
        for i, row in enumerate(reader, start=2):
            if len(data) >= settings.IMPORT_BATCH_SIZE:
                yield data
                data = []
            # Only text column
            if len(row) <= len(columns) and len(row) == 1:
                data.append({'text': row[0]})
            # Text, labels and metadata columns
            elif 2 <= len(row) <= len(columns):
                datum = dict(zip(columns, row))
                text, label = datum.pop('text'), datum.pop('label')
                meta = FileParser.encode_metadata(datum)
                if label != '':
                    j = {'text': text, 'labels': [label], 'meta': meta}
                else:
                    j = {'text': text, 'meta': meta}
                data.append(j)
            else:
                raise FileParseException(line_num=i, line=row)
        if data:
            yield data


class JSONParser(FileParser):

    def parse(self, file):
        file = EncodedIO(file)
        file = io.TextIOWrapper(file, encoding=file.encoding)
        data = []
        for i, line in enumerate(file, start=1):
            if len(data) >= settings.IMPORT_BATCH_SIZE:
                yield data
                data = []
            try:
                j = json.loads(line)
                j['meta'] = FileParser.encode_metadata(j.get('meta', {}))
                data.append(j)
            except json.decoder.JSONDecodeError:
                raise FileParseException(line_num=i, line=line)
        if data:
            yield data


class FastTextParser(FileParser):
    """
    Parse files in fastText format.
    Labels are marked with the __label__ prefix
    and the corresponding text comes afterwards in the same line
    For example:
    ```
    __label__dog poodle
    __label__house mansion
    ```
    """
    def parse(self, file):
        file = EncodedIO(file)
        file = io.TextIOWrapper(file, encoding=file.encoding)
        data = []
        for i, line in enumerate(file, start=0):
            if len(data) >= settings.IMPORT_BATCH_SIZE:
                yield data
                data = []

            # Search labels and text, check correct syntax and append
            labels = []
            text = []
            for token in line.rstrip().split(" "):
                if token.startswith('__label__'):
                    if token == '__label__':
                        raise FileParseException(line_num=i, line=line)
                    labels.append(token[len('__label__'):])
                else:
                    text.append(token)

            # Check if text for labels is given
            if not text:
                raise FileParseException(line_num=i, line=line)

            data.append({'text': " ".join(text), 'labels': labels})

        if data:
            yield data



class AudioParser(FileParser):
    def parse(self, file):
        file_type, _ = mimetypes.guess_type(file.name, strict=False)
        if not file_type:
            raise FileParseException(line_num=1, line='Unable to guess file type')

        audio = base64.b64encode(file.read())
        yield [{
            'audio': f'data:{file_type};base64,{audio.decode("ascii")}',
            'meta': json.dumps({'filename': file.name}),
        }]


class JSONLRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        if not isinstance(data, list):
            data = [data]

        for d in data:
            yield json.dumps(d,
                             cls=self.encoder_class,
                             ensure_ascii=self.ensure_ascii,
                             allow_nan=not self.strict) + '\n'


class FastTextPainter(object):

    @staticmethod
    def paint_labels(documents, labels):
        serializer = DocumentSerializer(documents, many=True)
        serializer_labels = LabelSerializer(labels, many=True)
        data = []
        for d in serializer.data:
            labels = []
            for a in d['annotations']:
                label_obj = [x for x in serializer_labels.data if x['id'] == a['label']][0]
                labels.append('__label__{}'.format(label_obj['text'].replace(' ', '_')))
            text = d['text'].replace('\n', ' ')
            if labels:
                data.append('{} {}'.format(' '.join(labels), text))
            else:
                data.append(text)
        return data


class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return bytes()

        if not isinstance(data, list):
            data = [data]

        buffer = io.BytesIO()
        for d in data:
            buffer.write((d + '\n').encode(self.charset))
        return buffer.getvalue()


class JSONPainter(object):

    def paint(self, documents):
        serializer = DocumentSerializer(documents, many=True)
        data = []
        for d in serializer.data:
            d['meta'] = json.loads(d['meta'])
            for a in d['annotations']:
                a.pop('id')
                a.pop('prob')
                a.pop('document')
            data.append(d)
        return data

    @staticmethod
    def paint_labels(documents, labels):
        serializer_labels = LabelSerializer(labels, many=True)
        serializer = DocumentSerializer(documents, many=True)
        data = []
        for d in serializer.data:
            labels = []
            for a in d['annotations']:
                label_obj = [x for x in serializer_labels.data if x['id'] == a['label']][0]
                label_text = label_obj['text']
                label_start = a['start_offset']
                label_end = a['end_offset']
                labels.append([label_start, label_end, label_text])
            d.pop('annotations')
            d['labels'] = labels
            d['meta'] = json.loads(d['meta'])
            data.append(d)
        return data


class CSVPainter(JSONPainter):

    def paint(self, documents):
        data = super().paint(documents)
        res = []
        for d in data:
            annotations = d.pop('annotations')
            for a in annotations:
                res.append({**d, **a})
        return res


def iterable_to_io(iterable, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """See https://stackoverflow.com/a/20260030/3817588."""
    class IterStream(io.RawIOBase):
        def __init__(self):
            self.leftover = None

        def readable(self):
            return True

        def readinto(self, b):
            try:
                l = len(b)  # We're supposed to return at most this much
                chunk = self.leftover or next(iterable)
                output, self.leftover = chunk[:l], chunk[l:]
                b[:len(output)] = output
                return len(output)
            except StopIteration:
                return 0    # indicate EOF

    return io.BufferedReader(IterStream(), buffer_size=buffer_size)


class EncodedIO(io.RawIOBase):
    def __init__(self, fobj, buffer_size=io.DEFAULT_BUFFER_SIZE, default_encoding='utf-8'):
        buffer = b''
        detector = UniversalDetector()

        while True:
            read = fobj.read(buffer_size)
            detector.feed(read)
            buffer += read
            if detector.done or len(read) < buffer_size:
                break

        if detector.done:
            self.encoding = detector.result['encoding']
        else:
            self.encoding = default_encoding

        self._fobj = fobj
        self._buffer = buffer

    def readable(self):
        return self._fobj.readable()

    def readinto(self, b):
        l = len(b)
        chunk = self._buffer or self._fobj.read(l)
        output, self._buffer = chunk[:l], chunk[l:]
        b[:len(output)] = output
        return len(output)
