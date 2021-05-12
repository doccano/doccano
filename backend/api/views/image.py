import random

from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Image, Project
from ..permissions import IsInProjectReadOnlyOrAdmin
from ..serializers import ImageSerializer


class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('filename',)
    ordering_fields = ('created_at', 'updated_at')
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])

        queryset = project.examples
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
        queryset = project.images
        delete_ids = request.data['ids']
        if delete_ids:
            queryset.filter(pk__in=delete_ids).delete()
        else:
            queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    lookup_url_kwarg = 'image_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]
