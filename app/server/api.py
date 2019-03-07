import csv
import io
import json
from collections import Counter

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .exceptions import FileParseException
from .filters import DocumentFilter
from .models import Project, Label, Document
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsOwnAnnotation
from .serializers import ProjectSerializer, LabelSerializer, DocumentSerializer
from .serializers import SequenceAnnotationSerializer, DocumentAnnotationSerializer, Seq2seqAnnotationSerializer
from .serializers import ProjectPolymorphicSerializer
from .utils import extract_label


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectPolymorphicSerializer
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
        label_count, user_count = self.label_per_data(p)
        progress = self.progress(project=p)
        response = dict()
        response['label'] = label_count
        response['user'] = user_count
        response.update(progress)
        return Response(response)

    def progress(self, project):
        total = project.documents.count()
        remaining = 0
        annotation_class = project.get_annotation_class()
        for d in project.documents.all():
            count = annotation_class.objects.filter(document=d).count()
            if count == 0:
                remaining += 1
        return {'total': total, 'remaining': remaining}

    def label_per_data(self, project):
        label_count = Counter()
        user_count = Counter()
        annotation_class = project.get_annotation_class()
        for doc in project.documents.all():
            annotations = annotation_class.objects.filter(document=doc.id)
            for a in annotations:
                label_count[a.label.text] += 1
                user_count[a.user.username] += 1
        return label_count, user_count


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
                       'seq_annotations__updated_at', 'seq2seq_annotations__updated_at')
    filter_class = DocumentFilter
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


class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()
        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        model = project.get_annotation_class()
        self.queryset = model.objects.filter(document=self.kwargs['doc_id'], user=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        serializer.save(document=doc, user=self.request.user)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'annotation_id'
    permission_classes = (IsAuthenticated, IsProjectUser, IsOwnAnnotation)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()
        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        model = project.get_annotation_class()
        self.queryset = model.objects.all()
        return self.queryset


class TextUploadAPI(APIView):
    """Base API for text upload."""
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            raise ParseError('Empty content')
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        handler = project.get_upload_handler(request.data['format'])
        handler.handle_uploaded_file(request.FILES['file'], self.request.user)
        return Response(status=status.HTTP_201_CREATED)


class TextDownloadAPI(APIView):
    """API for text download."""
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        format = request.query_params.get('q')
        project = get_object_or_404(Project, pk=project_id)
        handler = project.get_upload_handler(format)
        response = handler.render()
        return response


class FileHandler(object):
    annotation_serializer = None

    def __init__(self, project):
        self.project = project

    @transaction.atomic
    def handle_uploaded_file(self, file, user):
        raise NotImplementedError()

    def parse(self, file):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()

    def save_doc(self, data):
        serializer = DocumentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        doc = serializer.save(project=self.project)
        return doc

    def save_label(self, data):
        label = Label.objects.filter(project=self.project, **data).first()
        serializer = LabelSerializer(label, data=data)
        serializer.is_valid(raise_exception=True)
        label = serializer.save(project=self.project)
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
    def handle_uploaded_file(self, file, user):
        for words, tags in self.parse(file):
            start_offset = 0
            sent = ' '.join(words)
            doc = self.save_doc({'text': sent})
            for word, tag in zip(words, tags):
                label = extract_label(tag)
                label = self.save_label({'text': label})
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

    def render(self):
        raise ValidationError("This project type doesn't support CoNLL format.")


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
    def handle_uploaded_file(self, file, user):
        for text in self.parse(file):
            self.save_doc({'text': text})

    def parse(self, file):
        file = io.TextIOWrapper(file, encoding='utf-8')
        for i, line in enumerate(file, start=1):
            yield line.strip()

    def render(self):
        raise ValidationError("You cannot download plain text. Please specify csv or json.")


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
        columns = next(reader)
        for i, row in enumerate(reader, start=2):
            if len(row) == len(columns) and len(row) >= 2:
                text, label = row[:2]
                meta = json.dumps(dict(zip(columns[2:], row[2:])))
                data = {'text': text, 'meta': meta}
                yield data, label
            else:
                raise FileParseException(line_num=i, line=row)

    def render(self):
        queryset = self.project.documents.all()
        serializer = DocumentSerializer(queryset, many=True)
        filename = '_'.join(self.project.name.lower().split())
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
        writer = csv.writer(response)
        columns = ['id', 'text', 'label', 'user']
        meta_keys = self.get_meta_keys(serializer.data)
        columns.extend(meta_keys)
        writer.writerow(columns)
        for d in serializer.data:
            meta = json.loads(d['meta'])
            for a in d['annotations']:
                row = self.make_row(d, a)
                row.extend([meta[k] for k in meta_keys])
                writer.writerow(row)
        return response

    def get_meta_keys(self, data):
        if len(data):
            meta = json.loads(data[0]['meta'])
            return sorted(meta.keys())
        else:
            return []

    def make_row(self, doc, annotation):
        raise NotImplementedError('Please implement in subclass.')


class CSVClassificationHandler(CSVHandler):
    annotation_serializer = DocumentAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, user):
        for data, label in self.parse(file):
            doc = self.save_doc(data)
            label = self.save_label({'text': label})
            self.save_annotation({'label': label.id}, doc, user)

    def make_row(self, doc, annotation):
        row = [doc['id'], doc['text'], annotation['label'], annotation['user']]
        return row


class CSVSeq2seqHandler(CSVHandler):
    annotation_serializer = Seq2seqAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, user):
        for data, label in self.parse(file):
            doc = self.save_doc(data)
            self.save_annotation({'text': label}, doc, user)

    def make_row(self, doc, annotation):
        row = [doc['id'], doc['text'], annotation['text'], annotation['user']]
        return row


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
                j['meta'] = json.dumps(j.get('meta', {}))
                yield j
            except json.decoder.JSONDecodeError:
                raise FileParseException(line_num=i, line=line)

    def render(self):
        queryset = self.project.documents.all()
        serializer = DocumentSerializer(queryset, many=True)
        filename = '_'.join(self.project.name.lower().split())
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="{}.jsonl"'.format(filename)
        for d in serializer.data:
            d['meta'] = json.loads(d['meta'])
            dump = json.dumps(d, ensure_ascii=False)
            response.write(dump + '\n')
        return response


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
    def handle_uploaded_file(self, file, user):
        for data in self.parse(file):
            doc = self.save_doc(data)
            for label in data.get('labels', []):
                label = self.save_label({'text': label})
                self.save_annotation({'label': label.id}, doc, user)


class JsonLabelingHandler(JsonHandler):
    """Upload jsonl for sequence labeling.

    The format is as follows:
    ```
    {"text": "Python is awesome!", "labels": [[0, 6, "Product"],]}
    ...
    ```
    """
    annotation_serializer = SequenceAnnotationSerializer

    @transaction.atomic
    def handle_uploaded_file(self, file, user):
        for data in self.parse(file):
            doc = self.save_doc(data)
            for start_offset, end_offset, label in data.get('labels', []):
                label = self.save_label({'text': label})
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
    def handle_uploaded_file(self, file, user):
        for data in self.parse(file):
            doc = self.save_doc(data)
            for label in data.get('labels', []):
                self.save_annotation({'text': label}, doc, user)
