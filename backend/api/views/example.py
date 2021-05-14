import random

from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..filters import DocumentFilter
from ..models import Example, Project
from ..permissions import IsInProjectReadOnlyOrAdmin
from ..serializers import ExampleSerializer


class ExampleList(generics.ListCreateAPIView):
    serializer_class = ExampleSerializer
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = ('created_at', 'updated_at')
    model = Example

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_queryset(self):
        queryset = self.model.objects.filter(project=self.project)
        if self.project.random_order:
            # Todo: fix the algorithm.
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
    search_fields = ('text',)
    filter_class = DocumentFilter


class ImageList(ExampleList):
    search_fields = ('filename',)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    lookup_url_kwarg = 'doc_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    lookup_url_kwarg = 'image_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
