import abc
import random

from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..filters import DocumentFilter
from ..models import Document, Image, Project
from ..permissions import IsInProjectReadOnlyOrAdmin
from ..serializers import (DocumentSerializer, ExampleSerializer,
                           ImageSerializer)


class ExampleList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    @abc.abstractmethod
    def get_examples(self):
        raise NotImplementedError()

    def get_queryset(self):
        queryset = self.get_examples()
        if self.project.random_order:
            random.seed(self.request.user.id)
            value = random.randrange(2, 20)
            queryset = queryset.annotate(sort_id=F('id') % value).order_by('sort_id', 'id')
        else:
            queryset = queryset.order_by('id')
        return queryset

    def perform_create(self, serializer):
        serializer.save(project=self.project)

    def delete(self, request, *args, **kwargs):
        queryset = self.project.examples
        delete_ids = request.data['ids']
        if delete_ids:
            queryset.filter(pk__in=delete_ids).delete()
        else:
            queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentList(ExampleList):
    serializer_class = ExampleSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text',)
    ordering_fields = ('created_at', 'updated_at', 'doc_annotations__updated_at',
                       'seq_annotations__updated_at', 'seq2seq_annotations__updated_at')
    filter_class = DocumentFilter
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_examples(self):
        queryset = self.project.examples.instance_of(Document)
        queryset.model = Document
        return queryset


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_url_kwarg = 'doc_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class ImageList(ExampleList):
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('filename',)
    ordering_fields = ('created_at', 'updated_at')
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_examples(self):
        queryset = self.project.examples.instance_of(Image)
        queryset.model = Image
        return queryset


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_url_kwarg = 'image_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
