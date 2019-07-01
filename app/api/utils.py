import csv
import io
import itertools
import json
import re
from collections import defaultdict
from random import Random

from django.db import transaction
from django.conf import settings
from rest_framework.renderers import JSONRenderer
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
    def to_serializer_format(cls, labels, created, random_seed=None):
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

            color = Color.random(seed=random_seed)
            serializer_label['background_color'] = color.hex
            serializer_label['text_color'] = color.contrast_color.hex

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


class FileParser(object):

    def parse(self, file):
        raise NotImplementedError()


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
        words, tags = [], []
        data = []
        file = io.TextIOWrapper(file, encoding='utf-8')
        for i, line in enumerate(file, start=1):
            if len(data) >= settings.IMPORT_BATCH_SIZE:
                yield data
                data = []
            line = line.strip()
            if line:
                try:
                    word, tag = line.split('\t')
                except ValueError:
                    raise FileParseException(line_num=i, line=line)
                words.append(word)
                tags.append(tag)
            elif words and tags:
                j = self.calc_char_offset(words, tags)
                data.append(j)
                words, tags = [], []
        if len(words) > 0:
            j = self.calc_char_offset(words, tags)
            data.append(j)
        if data:
            yield data

    @classmethod
    def calc_char_offset(cls, words, tags):
        doc = ' '.join(words)
        j = {'text': ' '.join(words), 'labels': []}
        pos = defaultdict(int)
        for label, start_offset, end_offset in get_entities(tags):
            entity = ' '.join(words[start_offset: end_offset + 1])
            char_left = doc.index(entity, pos[entity])
            char_right = char_left + len(entity)
            span = [char_left, char_right, label]
            j['labels'].append(span)
            pos[entity] = char_right
        return j


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
        file = io.TextIOWrapper(file, encoding='utf-8')
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
        file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(file)
        columns = next(reader)
        data = []
        for i, row in enumerate(reader, start=2):
            if len(data) >= settings.IMPORT_BATCH_SIZE:
                yield data
                data = []
            if len(row) == len(columns) and len(row) >= 2:
                text, label = row[:2]
                meta = json.dumps(dict(zip(columns[2:], row[2:])))
                j = {'text': text, 'labels': [label], 'meta': meta}
                data.append(j)
            else:
                raise FileParseException(line_num=i, line=row)
        if data:
            yield data


class JSONParser(FileParser):

    def parse(self, file):
        file = io.TextIOWrapper(file, encoding='utf-8')
        data = []
        for i, line in enumerate(file, start=1):
            if len(data) >= settings.IMPORT_BATCH_SIZE:
                yield data
                data = []
            try:
                j = json.loads(line)
                #j  = json.loads(line.decode('utf-8'))
                j['meta'] = json.dumps(j.get('meta', {}))
                data.append(j)
            except json.decoder.JSONDecodeError:
                raise FileParseException(line_num=i, line=line)
        if data:
            yield data


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


class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def contrast_color(self):
        """Generate black or white color.

        Ensure that text and background color combinations provide
        sufficient contrast when viewed by someone having color deficits or
        when viewed on a black and white screen.

        Algorithm from w3c:
        * https://www.w3.org/TR/AERT/#color-contrast
        """
        return Color.white() if self.brightness < 128 else Color.black()

    @property
    def brightness(self):
        return ((self.red * 299) + (self.green * 587) + (self.blue * 114)) / 1000

    @property
    def hex(self):
        return '#{:02x}{:02x}{:02x}'.format(self.red, self.green, self.blue)

    @classmethod
    def white(cls):
        return cls(red=255, green=255, blue=255)

    @classmethod
    def black(cls):
        return cls(red=0, green=0, blue=0)

    @classmethod
    def random(cls, seed=None):
        rgb = Random(seed).choices(range(256), k=3)
        return cls(*rgb)


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
