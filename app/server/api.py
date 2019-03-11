from collections import Counter

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import generics, filters, status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework_csv.renderers import CSVRenderer

from .filters import DocumentFilter
from .models import Project, Label, Document
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsOwnAnnotation
from .serializers import ProjectSerializer, LabelSerializer, DocumentSerializer
from .serializers import ProjectPolymorphicSerializer
from .utils import CSVParser, JSONParser, PlainTextParser, CoNLLParser
from .utils import JSONLRenderer
from .utils import JSONPainter, CSVPainter


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectPolymorphicSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, IsAdminUserAndWriteOnly)

    def get_queryset(self):
        return self.request.user.projects

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])


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
        docs = project.documents
        annotation_class = project.get_annotation_class()
        total = docs.count()
        done = annotation_class.objects.filter(document_id__in=docs.all()).\
            aggregate(Count('document', distinct=True))['document__count']
        remaining = total - done
        return {'total': total, 'remaining': remaining}

    def label_per_data(self, project):
        label_count = Counter()
        user_count = Counter()
        annotation_class = project.get_annotation_class()
        docs = project.documents.all()
        annotations = annotation_class.objects.filter(document_id__in=docs.all())
        for d in annotations.values('label__text', 'user__username').annotate(Count('label'), Count('user')):
            label_count[d['label__text']] += d['label__count']
            user_count[d['user__username']] += d['user__count']
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
        self.queryset = model.objects.filter(document=self.kwargs['doc_id'],
                                             user=self.request.user)
        return self.queryset

    def create(self, request, *args, **kwargs):
        request.data['document'] = self.kwargs['doc_id']
        return super().create(request, args, kwargs)

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
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content')
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        parser = self.select_parser(request.data['format'])
        data = parser.parse(request.data['file'])
        storage = project.get_storage(data)
        storage.save(self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    def select_parser(self, format):
        if format == 'plain':
            return PlainTextParser()
        elif format == 'csv':
            return CSVParser()
        elif format == 'json':
            return JSONParser()
        elif format == 'conll':
            return CoNLLParser()
        else:
            raise ValidationError('format {} is invalid.'.format(format))


class TextDownloadAPI(APIView):
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)
    renderer_classes = (CSVRenderer, JSONLRenderer)

    def get(self, request, *args, **kwargs):
        format = request.query_params.get('q')
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        documents = project.documents.all()
        painter = self.select_painter(format)
        data = painter.paint(documents)
        return Response(data)

    def select_painter(self, format):
        if format == 'csv':
            return CSVPainter()
        elif format == 'json':
            return JSONPainter()
        else:
            raise ValidationError('format {} is invalid.'.format(format))
