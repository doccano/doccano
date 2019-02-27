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
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsMyEntity
from .serializers import ProjectSerializer, LabelSerializer, DocumentSerializer
from .serializers import SequenceAnnotationSerializer


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
        self.handle_uploaded_file(request.FILES['file'])
        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def handle_uploaded_file(self, file):
        raise NotImplementedError()

    def parse(self, file):
        raise NotImplementedError()


class CoNLLFileUploadAPI(TextUploadAPI):
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

    @transaction.atomic
    def handle_uploaded_file(self, file):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        for words in self.parse(file):
            sent = self.words_to_sent(words)
            data = {'text': sent}
            serializer = DocumentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)

    def words_to_sent(self, words):
        return ' '.join(words)

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
                yield words
                words, tags = [], []
        if len(words) > 0:
            yield words


class PlainTextUploadAPI(TextUploadAPI):
    """Uploads plain text.

    The file format is as follows:
    ```
    EU rejects German call to boycott British lamb.
    President Obama is speaking at the White House.
    ...
    ```
    """
    @transaction.atomic
    def handle_uploaded_file(self, file):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        for text in self.parse(file):
            data = {'text': text}
            serializer = DocumentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)

    def parse(self, file):
        file = io.TextIOWrapper(file, encoding='utf-8')
        for i, line in enumerate(file, start=1):
            yield line.strip()


class CSVUploadAPI(TextUploadAPI):
    """Uploads csv file.

    The file format is comma separated values.
    Column names are required at the top of a file.
    For example:
    ```
    text, label(optional)
    "EU rejects German call to boycott British lamb.",
    "President Obama is speaking at the White House.",
    "He lives in Newark, Ohio.",
    ...
    ```
    """

    @transaction.atomic
    def handle_uploaded_file(self, file):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        for text, label in self.parse(file):
            data = {'text': text}
            serializer = DocumentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)

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


class JSONLUploadAPI(TextUploadAPI):
    """Uploads jsonl file.

    The file format is as follows:
    ```
    {"text": "example1"}
    {"text": "example2"}
    ...
    ```
    """

    @transaction.atomic
    def handle_uploaded_file(self, file):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        for data in self.parse(file):
            serializer = DocumentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)

    def parse(self, file):
        for i, line in enumerate(file, start=1):
            try:
                j = json.loads(line)
                yield j
            except json.decoder.JSONDecodeError:
                raise FileParseException(line_num=i, line=line)
