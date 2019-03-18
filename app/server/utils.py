import csv
import io
import itertools
import json
import re
from collections import defaultdict

from django.db import transaction
from rest_framework.renderers import JSONRenderer
from seqeval.metrics.sequence_labeling import get_entities

from app.settings import IMPORT_BATCH_SIZE
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

    def extract_label(self, data):
        """Extract labels from parsed data.

        Example:
            >>> data = [{"labels": ["positive"]}, {"labels": ["negative"]}]
            >>> self.extract_label(data)
            [["positive"], ["negative"]]
        """
        return [d.get('labels', []) for d in data]

    def exclude_created_labels(self, labels, created):
        """Exclude created labels.

        Example:
            >>> labels = ["positive", "negative"]
            >>> created = {"positive": ...}
            >>> self.exclude_created_labels(labels, created)
            ["negative"]
        """
        return [label for label in labels if label not in created]

    def to_serializer_format(self, labels):
        """Exclude created labels.

        Example:
            >>> labels = ["positive"]
            >>> self.to_serializer_format(labels)
            [{"text": "negative"}]
        ```
        """
        return [{'text': label} for label in labels]

    def update_saved_labels(self, saved, new):
        """Update saved labels.

        Example:
            >>> saved = {'positive': ...}
            >>> new = [<Label: positive>]
        """
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
            unique_labels = self.to_serializer_format(unique_labels)
            new_labels = self.save_label(unique_labels)
            saved_labels = self.update_saved_labels(saved_labels, new_labels)
            annotations = self.make_annotations(docs, labels, saved_labels)
            self.save_annotation(annotations, user)

    def extract_unique_labels(self, labels):
        """Extract unique labels

        Example:
            >>> labels = [["positive"], ["positive", "negative"], ["negative"]]
            >>> self.extract_unique_labels(labels)
            ["positive", "negative"]
        """
        return set(itertools.chain(*labels))

    def make_annotations(self, docs, labels, saved_labels):
        """Make list of annotation obj for serializer.

        Example:
            >>> docs = ["<Document: a>", "<Document: b>", "<Document: c>"]
            >>> labels = [["positive"], ["positive", "negative"], ["negative"]]
            >>> saved_labels = {"positive": "<Label: positive>", 'negative': "<Label: negative>"}
            >>> self.make_annotations(docs, labels, saved_labels)
            [{"document": 1, "label": 1}, {"document": 2, "label": 1}
            {"document": 2, "label": 2}, {"document": 3, "label": 2}]
        """
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
            unique_labels = self.to_serializer_format(unique_labels)
            new_labels = self.save_label(unique_labels)
            saved_labels = self.update_saved_labels(saved_labels, new_labels)
            annotations = self.make_annotations(docs, labels, saved_labels)
            self.save_annotation(annotations, user)

    def extract_unique_labels(self, labels):
        """Extract unique labels

        Example:
            >>> labels = [[[0, 1, "LOC"]], [[3, 4, "ORG"]]]
            >>> self.extract_unique_labels(labels)
            ["LOC", "ORG"]
        """
        return set([label for _, _, label in itertools.chain(*labels)])

    def make_annotations(self, docs, labels, saved_labels):
        """Make list of annotation obj for serializer.

        Example:
            >>> docs = ["<Document: a>", "<Document: b>"]
            >>> labels = labels = [[[0, 1, "LOC"]], [[3, 4, "ORG"]]]
            >>> saved_labels = {"LOC": "<Label: LOC>", 'ORG': "<Label: ORG>"}
            >>> self.make_annotations(docs, labels, saved_labels)
            [
              {"document": 1, "label": 1, "start_offset": 0, "end_offset": 1}
              {"document": 2, "label": 2, "start_offset": 3, "end_offset": 4}
            ]
        """
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

    def make_annotations(self, docs, labels):
        """Make list of annotation obj for serializer.

        Example:
            >>> docs = ["<Document: a>", "<Document: b>"]
            >>> labels = [["Hello!"], ["How are you?", "What's up?"]]
            >>> self.make_annotations(docs, labels)
            [{"document": 1, "text": "Hello"}, {"document": 2, "text": "How are you?"}
            {"document": 2, "text": "What's up?"}]
        """
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
        """Store json for seq2seq.

        Return format:
        {"text": "Python is awesome!", "labels": [[0, 6, "Product"],]}
        ...
        """
        words, tags = [], []
        data = []
        for i, line in enumerate(file, start=1):
            if len(data) >= IMPORT_BATCH_SIZE:
                yield data
                data = []
            line = line.decode('utf-8')
            line = line.strip()
            if line:
                try:
                    word, tag = line.split('\t')
                except ValueError:
                    raise FileParseException(line_num=i, line=line)
                words.append(word)
                tags.append(tag)
            else:
                j = self.calc_char_offset(words, tags)
                data.append(j)
                words, tags = [], []
        if len(words) > 0:
            j = self.calc_char_offset(words, tags)
            data.append(j)
            yield data

    def calc_char_offset(self, words, tags):
        """
        Examples:
            >>> words = ['EU', 'rejects', 'German', 'call']
            >>> tags = ['B-ORG', 'O', 'B-MISC', 'O']
            >>> entities = get_entities(tags)
            >>> entities
            [['ORG', 0, 0], ['MISC', 2, 2]]
            >>> self.calc_char_offset(words, tags)
            {
              'text': 'EU rejects German call',
              'labels': [[0, 2, 'ORG'], [11, 17, 'MISC']]
            }
        """
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
            batch = list(itertools.islice(file, IMPORT_BATCH_SIZE))
            if not batch:
                raise StopIteration
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
            if len(data) >= IMPORT_BATCH_SIZE:
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
        data = []
        for i, line in enumerate(file, start=1):
            if len(data) >= IMPORT_BATCH_SIZE:
                yield data
                data = []
            try:
                j = json.loads(line)
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


class CSVPainter(JSONPainter):

    def paint(self, documents):
        data = super().paint(documents)
        res = []
        for d in data:
            annotations = d.pop('annotations')
            for a in annotations:
                res.append({**d, **a})
        return res
