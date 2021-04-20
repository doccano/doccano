import random

from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..filters import DocumentFilter
from ..models import Document, Project
from ..permissions import IsInProjectReadOnlyOrAdmin
from ..serializers import DocumentSerializer


class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text',)
    ordering_fields = ('created_at', 'updated_at', 'doc_annotations__updated_at',
                       'seq_annotations__updated_at', 'seq2seq_annotations__updated_at')
    filter_class = DocumentFilter
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])

        queryset = project.documents
        if project.randomize_document_order:
            random.seed(self.request.user.id)
            value = random.randrange(2, 20)
            queryset = queryset.annotate(sort_id=F('id') % value).order_by('sort_id', 'id')
        else:
            queryset = queryset.order_by('id')

        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        queryset = project.documents
        delete_ids = request.data['ids']
        if delete_ids:
            queryset.filter(pk__in=delete_ids).delete()
        else:
            queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_url_kwarg = 'doc_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
