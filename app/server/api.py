from collections import Counter

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .filters import DocumentFilter
from .models import Project, Label, Document
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsOwnAnnotation
from .serializers import ProjectSerializer, LabelSerializer, DocumentSerializer
from .serializers import ProjectPolymorphicSerializer


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
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content')
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        handler = project.get_file_handler(request.data['format'])
        handler.handle_uploaded_file(request.data['file'], self.request.user)
        return Response(status=status.HTTP_201_CREATED)


class TextDownloadAPI(APIView):
    permission_classes = (IsAuthenticated, IsProjectUser, IsAdminUser)

    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        format = request.query_params.get('q')
        project = get_object_or_404(Project, pk=project_id)
        handler = project.get_file_handler(format)
        response = handler.render()
        return response
