from collections import Counter
from itertools import chain

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Label, Document
from .models import SequenceAnnotation
from .permissions import IsAdminUserAndWriteOnly, IsProjectUser, IsOwnAnnotation
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
        queryset = self.queryset.filter(document=self.kwargs['doc_id'])
        return queryset

    def perform_create(self, serializer):
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        serializer.save(document=doc, user=self.request.user)


class EntityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SequenceAnnotation.objects.all()
    serializer_class = SequenceAnnotationSerializer
    lookup_url_kwarg = 'entity_id'
    permission_classes = (IsAuthenticated, IsProjectUser)


class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticated, IsProjectUser)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()

        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        document = project.documents.get(id=self.kwargs['doc_id'])
        self.queryset = document.get_annotations()
        self.queryset = self.queryset.filter(user=self.request.user)

        return self.queryset

    def perform_create(self, serializer):
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        serializer.save(document=doc, user=self.request.user)


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsProjectUser, IsOwnAnnotation)

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()

        return self.serializer_class

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        self.queryset = document.get_annotations()

        return self.queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.kwargs['annotation_id'])
        self.check_object_permissions(self.request, obj)

        return obj
