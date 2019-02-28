import csv
import io
import json
from collections import Counter
from itertools import chain

from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .exceptions import FileParseException
from .models import Project, Label, Document
from .models import SequenceAnnotation
from .models import DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsMyEntity
from .serializers import ProjectSerializer, LabelSerializer, DocumentSerializer
from .serializers import SequenceAnnotationSerializer, DocumentAnnotationSerializer, Seq2seqAnnotationSerializer
from .utils import extract_label


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        return self.request.user.projects

    def create(self, request, *args, **kwargs):
        request.data['users'] = [self.request.user.id]
        return super().create(request, args, kwargs)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_url_kwarg = 'project_id'
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)


class StatisticsAPI(APIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])
        labels = [label.text for label in p.labels.all()]
        users = [user.username for user in p.users.all()]
        docs = [doc for doc in p.documents.all()]
        nested_labels = [[a.label.text for a in doc.get_annotations()] for doc in docs]
        nested_users = [[a.user.username for a in doc.get_annotations()] for doc in docs]

        label_count = Counter(chain(*nested_labels))
        label_data = [label_count[name] for name in labels]

        user_count = Counter(chain(*nested_users))
        user_data = [user_count[name] for name in users]

        response = {'label': {'labels': labels, 'data': label_data},
                    'user': {'users': users, 'data': user_data}}

        return Response(response)


class LabelList(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs['project_id'])
        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    lookup_url_kwarg = 'label_id'
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text', )
    ordering_fields = ('created_at', 'updated_at', 'doc_annotations__updated_at',
                       'seq_annotations__updated_at')
    filter_fields = ('doc_annotations__label__id', 'seq_annotations__label__id')
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        queryset = self.queryset.filter(project=self.kwargs['project_id'])
        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_url_kwarg = 'doc_id'
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUserAndWriteOnly)


class EntityList(generics.ListCreateAPIView):
    queryset = SequenceAnnotation.objects.all()
    serializer_class = SequenceAnnotationSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get_queryset(self):
        queryset = self.queryset.filter(document=self.kwargs['doc_id'],
                                        user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        serializer.save(document=doc, user=self.request.user)


class EntityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SequenceAnnotation.objects.all()
    serializer_class = SequenceAnnotationSerializer
    lookup_url_kwarg = 'entity_id'
    permission_classes = (IsAuthenticated, IsProjectUser, IsMyEntity)


class TextUploadAPI(APIView):
    """Base API for text upload."""
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            raise ParseError('Empty content')
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        handler = self.decide_handler(request.data['format'], project.project_type)
        handler.handle_uploaded_file(request.FILES['file'], project, self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    def decide_handler(self, format, project_type):
        if format == 'plain':
            return PlainTextHandler()
        elif format == 'conll' and project_type:
            return CoNLLHandler()
        elif format == 'csv':
            if project_type == DOCUMENT_CLASSIFICATION:
                return CSVClassificationHandler()
            elif project_type == SEQ2SEQ:
                return CSVSeq2seqHandler()
        elif format == 'json':
            if project_type == DOCUMENT_CLASSIFICATION:
                return JsonClassificationHandler()
            elif project_type == SEQUENCE_LABELING:
                return JsonLabelingHandler()
            elif project_type == SEQ2SEQ:
                return JsonSeq2seqHandler()
        raise ValueError('format {} is invalid.'.format(format))


class FileHandler(object):
    annotation_serializer = None

    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        raise NotImplementedError()

    def parse(self, file):
        raise NotImplementedError()

    def save_doc(self, data, project):
        serializer = DocumentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        doc = serializer.save(project=project)
        return doc

    def save_label(self, data, project):
        label = Label.objects.filter(project=project, **data).first()
        serializer = LabelSerializer(label, data=data)
        serializer.is_valid(raise_exception=True)
        label = serializer.save(project=project)
        return label

    def save_annotation(self, data, doc, user):
        serializer = self.annotation_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        annotation = serializer.save(document=doc, user=user)
        return annotation


class CoNLLHandler(FileHandler):
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
    annotation_serializer = SequenceAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        for words, tags in self.parse(file):
            start_offset = 0
            sent = ' '.join(words)
            doc = self.save_doc({'text': sent}, project)
            for word, tag in zip(words, tags):
                label = extract_label(tag)
                label = self.save_label({'text': label}, project)
                data = {'start_offset': start_offset,
                        'end_offset': start_offset + len(word),
                        'label': label.id}
                start_offset += len(word) + 1
                self.save_annotation(data, doc, user)

    def parse(self, file):
        words, tags = [], []
        for i, line in enumerate(file, start=1):
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
                yield words, tags
                words, tags = [], []
        if len(words) > 0:
            yield words, tags


class PlainTextHandler(FileHandler):
    """Uploads plain text.

    The file format is as follows:
    ```
    EU rejects German call to boycott British lamb.
    President Obama is speaking at the White House.
    ...
    ```
    """
    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        for text in self.parse(file):
            self.save_doc({'text': text}, project)

    def parse(self, file):
        file = io.TextIOWrapper(file, encoding='utf-8')
        for i, line in enumerate(file, start=1):
            yield line.strip()


class CSVHandler(FileHandler):
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
        columns = None
        for i, row in enumerate(reader, start=1):
            if i == 1:                           # skip header
                columns = row
                continue
            elif len(row) == len(columns) == 2:  # text with a label
                text, label = row
                yield text, label
            else:
                raise FileParseException(line_num=i, line=row)


class CSVClassificationHandler(CSVHandler):
    annotation_serializer = DocumentAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        for text, label in self.parse(file):
            doc = self.save_doc({'text': text}, project)
            label = self.save_label({'text': label}, project)
            self.save_annotation({'label': label.id}, doc, user)


class CSVSeq2seqHandler(CSVHandler):
    annotation_serializer = Seq2seqAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        for text, label in self.parse(file):
            doc = self.save_doc({'text': text}, project)
            self.save_annotation({'text': label}, doc, user)


class JsonHandler(FileHandler):
    """Uploads jsonl file.

    The file format is as follows:
    ```
    {"text": "example1"}
    {"text": "example2"}
    ...
    ```
    """
    def parse(self, file):
        for i, line in enumerate(file, start=1):
            try:
                j = json.loads(line)
                yield j
            except json.decoder.JSONDecodeError:
                raise FileParseException(line_num=i, line=line)


class JsonClassificationHandler(JsonHandler):
    """Upload jsonl for text classification.

    The format is as follows:
    ```
    {"text": "Python is awesome!", "labels": ["positive"]}
    ...
    ```
    """
    annotation_serializer = DocumentAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        for data in self.parse(file):
            doc = self.save_doc(data, project)
            for label in data['labels']:
                label = self.save_label({'text': label}, project)
                self.save_annotation({'label': label.id}, doc, user)


class JsonLabelingHandler(JsonHandler):
    """Upload jsonl for sequence labeling.

    The format is as follows:
    ```
    {"text": "Python is awesome!", "entities": [[0, 6, "Product"],]}
    ...
    ```
    """
    annotation_serializer = SequenceAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        for data in self.parse(file):
            doc = self.save_doc(data, project)
            for start_offset, end_offset, label in data['entities']:
                label = self.save_label({'text': label}, project)
                data = {'label': label.id,
                        'start_offset': start_offset,
                        'end_offset': end_offset}
                self.save_annotation(data, doc, user)


class JsonSeq2seqHandler(JsonHandler):
    """Upload jsonl for seq2seq.

    The format is as follows:
    ```
    {"text": "Hello, World!", "labels": ["こんにちは、世界!"]}
    ...
    ```
    """
    annotation_serializer = Seq2seqAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, project, user):
        for data in self.parse(file):
            doc = self.save_doc(data, project)
            for label in data['labels']:
                self.save_annotation({'text': label}, doc, user)
